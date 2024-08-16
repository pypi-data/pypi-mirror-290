
import numpy as np
import pandas as pd
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, TensorDataset
from prettytable import PrettyTable
from sklearn.decomposition import PCA
import shap
from scipy.stats import kendalltau
from scipy.stats import spearmanr
import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression


# 定义一个三层全连接神经网络
class ThreeLayerNet(nn.Module):
    def __init__(self, input_size):
        super(ThreeLayerNet, self).__init__()
        self.fc1 = nn.Linear(input_size, 16)  # 第一层，64个神经元
        self.fc2 = nn.Linear(16, 8)  # 第二层，32个神经元
        self.fc3 = nn.Linear(8, 1)  # 第三层，输出1个神经元

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class EarlyStopping:
    def __init__(self, model_path, patience=5, verbose=False):
        self.model_path = model_path
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_loss = float('inf')
        self.early_stop = False

    def __call__(self, val_loss, model):
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.counter = 0
            if self.verbose:
                print(f'Validation loss decreased ({self.best_loss:.6f} < {val_loss:.6f}). Saving model...')
            torch.save(model.state_dict(), self.model_path)
        else:
            self.counter += 1
            if self.verbose:
                print(f'Validation loss did not decrease. Counter: {self.counter}/{self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True


class distilltower:
    def __init__(self, train, predict, data_path, describe_path, model_path='distill-tower'):
        """initialize the model"""
        self.train = train
        self.predict = predict
        self.data_path = data_path
        self.describe_path = describe_path
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        """fix the random seed"""
        seed = 2020
        # random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def rank_order(self, arr):
        unique_elements = sorted(set(arr))
        rank_dict = {element: rank for rank, element in enumerate(unique_elements, start=1)}
        return np.array([rank_dict[element] for element in arr])

    def calculate_weighted_score(self, scores, arr, weights, n):
        for i, element in enumerate(arr):
            scores[element] = scores.get(element, 0) + (n - i) * weights
        return scores

    def merge_rankings_with_spearman(self, filtered_list):
        n = len(filtered_list)
        num_elements = len(filtered_list[0])
        spearman_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    spearman_matrix[i, j] = 1.0
                else:
                    rho, _ = spearmanr(filtered_list[i], filtered_list[j])
                    spearman_matrix[i, j] = rho
                    spearman_matrix[j, i] = rho

        weights = np.mean(spearman_matrix, axis=1)
        scores = {element: 0 for element in filtered_list[0]}

        for i, ranking in enumerate(filtered_list):
            weight = weights[i]
            for j, element in enumerate(ranking):
                scores[element] += (num_elements - j) * weight

        sorted_elements = np.array(sorted(scores.items(), key=lambda item: item[1], reverse=True))

        return sorted_elements

    def process(self):
        dt = pd.read_excel(self.data_path, sheet_name="Sheet1")
        dt = dt.to_numpy()
        dt = torch.tensor(dt, dtype=torch.float32).to(self.device)

        input_variables = len(dt[0, :-1])

        dataset = TensorDataset(dt[:, :input_variables], dt[:, input_variables:])
        # 定义训练集和测试集的大小
        train_size = int(0.8 * len(dt))
        test_size = len(dt) - train_size
        train_dataset, test_dataset = random_split(dataset, [train_size, test_size])
        train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

        """# Create the ANN"""

        model = ThreeLayerNet(input_variables).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        early_stopping = EarlyStopping(self.model_path, patience=10, verbose=True)
        if self.train:
            num_epochs = 1000
            for epoch in range(num_epochs):
                mf_loss_total = 0
                model.train()
                train_cf_s = time.time()
                for data, labels in train_loader:
                    # 前向传播
                    output = model(data)
                    loss = criterion(output, labels)

                    # 反向传播和优化
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    mf_loss_total += loss.item()
                mf_loss_total = mf_loss_total / len(train_loader)
                train_cf_e = time.time()

                # 打印损失
                if epoch % 10 == 0:
                    model.eval()
                    total_loss = 0
                    with torch.no_grad():
                        for inputs, targets in test_loader:
                            # 前向传播
                            outputs = model(inputs)
                            loss = criterion(outputs, targets)
                            total_loss += loss.item()

                    avg_loss = total_loss / len(test_loader)
                    print(f'Epoch [{epoch}/{num_epochs}], Test Loss: {avg_loss:.4f}')
                    early_stopping(avg_loss, model)
                    if early_stopping.early_stop:
                        print('Early stopping triggered')
                        break
                else:
                    print('Epoch [%d/%d], using time %.4f, training loss at epoch %d: %.4f' % (
                    epoch, num_epochs, train_cf_e - train_cf_s, epoch, mf_loss_total))

        if self.predict:
            model.load_state_dict(torch.load(self.model_path))
            model.eval()
            data = test_dataset[0][0]
            label = test_dataset[0][1]
            output = model(data)
            loss = criterion(output, label)
            print(f'predict data:{data}\nlabel:{label}\npredicted value: {output}, loss: {loss}')
            layers1 = model.fc1
            layers2 = model.fc2
            layers3 = model.fc3
            w1 = layers1.weight.detach().cpu().numpy()
            w2 = layers2.weight.detach().cpu().numpy()
            w3 = layers3.weight.detach().cpu().numpy()

            total_importance = np.zeros(21)
            for i in range(21):
                for j in range(16):
                    for k in range(8):
                        total_importance[i] += np.abs(w1[j, i]) * np.abs(w2[k, j]) * np.abs(w3[0, k])

            dt_describe = pd.read_excel(self.describe_path, sheet_name="Sheet1", header=None)[0]
            important_model = np.vstack((dt_describe.to_numpy(), total_importance)).T
            sorted_indices = np.argsort(important_model[:, -1])[::-1]
            important_model = important_model[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names =['name', 'importance']
            for i in important_model:
                train_res.add_row(i)
            print("Input feature importance:\n", train_res)

            pca = PCA()
            pca.fit(train_dataset[:][0].detach().cpu().numpy())
            components = pca.components_
            feature_importance = np.abs(np.mean(components, 0))
            feature_importance /= np.sum(feature_importance)
            important_pca = np.vstack((dt_describe.to_numpy(), feature_importance)).T
            sorted_indices = np.argsort(important_pca[:, -1])[::-1]
            important_pca = important_pca[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_pca:
                train_res.add_row(i)
            print("PCA importance:\n", train_res)

            # 定义SHAP解释器
            explainer = shap.DeepExplainer(model, train_dataset[:100][0])  # 这里的model在准备工作中已经完成建模，模型名称就是model
            shap_values = explainer.shap_values(test_dataset[100:103][0], check_additivity=False)
            # explainer = shap.KernelExplainer(model.forward, shap.sample(train_dataset[:][0], 100), link='logit')
            # shap_values = explainer.shap_values(train_dataset[:][0])
            # shap_values = shap_values.mean(0).__abs__()
            shap_values = shap_values.mean(0)
            shap_values = np.abs(shap_values)
            important_shap = np.vstack((dt_describe.to_numpy(), shap_values)).T
            sorted_indices = np.argsort(important_shap[:, -1])[::-1]
            important_shap = important_shap[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_shap:
                train_res.add_row(i)
            print("SHAP importance:\n", train_res)

            model_dt = DecisionTreeRegressor(random_state=2020)  # 或者使用 DecisionTreeClassifier 如果是分类问题
            model_dt.fit(train_dataset[:][0].detach().cpu().numpy(), train_dataset[:][1].detach().cpu().numpy())
            feature_importances = np.abs(model_dt.feature_importances_)
            important_dt = np.vstack((dt_describe.to_numpy(), feature_importances)).T
            sorted_indices = np.argsort(important_dt[:, -1])[::-1]
            important_dt = important_dt[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_dt:
                train_res.add_row(i)
            print("DT importance:\n", train_res)

            model_rf = RandomForestRegressor()
            model_rf.fit(train_dataset[:][0].detach().cpu().numpy(), train_dataset[:][1].detach().cpu().numpy().ravel())
            feature_importances = np.abs(model_rf.feature_importances_)
            important_rf = np.vstack((dt_describe.to_numpy(), feature_importances)).T
            sorted_indices = np.argsort(important_rf[:, -1])[::-1]
            important_rf = important_rf[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_rf:
                train_res.add_row(i)
            print("RF importance:\n", train_res)

            model_gb = GradientBoostingRegressor()
            model_gb.fit(train_dataset[:][0].detach().cpu().numpy(), train_dataset[:][1].detach().cpu().numpy().ravel())
            feature_importances = np.abs(model_gb.feature_importances_)
            important_gb = np.vstack((dt_describe.to_numpy(), feature_importances)).T
            sorted_indices = np.argsort(important_gb[:, -1])[::-1]
            important_gb = important_gb[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_gb:
                train_res.add_row(i)
            print("GB importance:\n", train_res)

            model_lg = LinearRegression()
            model_lg.fit(train_dataset[:][0].detach().cpu().numpy(), train_dataset[:][1].detach().cpu().numpy())
            feature_importances = np.abs(model_lg.coef_)
            important_lg = np.vstack((dt_describe.to_numpy(), feature_importances)).T
            sorted_indices = np.argsort(important_lg[:, -1])[::-1]
            important_lg = important_lg[sorted_indices]
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in important_lg:
                train_res.add_row(i)
            print("LG importance:\n", train_res)

            similar = []
            spearman_corr, _ = spearmanr(important_model[:, 0], important_pca[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_pca[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-pca: ", spearman_corr, tau)
            spearman_corr, _ = spearmanr(important_model[:, 0], important_shap[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_shap[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-shap: ", spearman_corr, tau)
            spearman_corr, _ = spearmanr(important_model[:, 0], important_dt[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_dt[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-dt: ", spearman_corr, tau)
            spearman_corr, _ = spearmanr(important_model[:, 0], important_rf[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_rf[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-rf: ", spearman_corr, tau)
            spearman_corr, _ = spearmanr(important_model[:, 0], important_gb[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_gb[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-gb: ", spearman_corr, tau)
            spearman_corr, _ = spearmanr(important_model[:, 0], important_lg[:, 0])
            tau, _ = kendalltau(important_model[:, 0], important_lg[:, 0])
            similar.append(spearman_corr)
            print("重要度分级相似度-lg: ", spearman_corr, tau)
            important_all = [important_pca[:, 0], important_shap[:, 0], important_dt[:, 0], important_rf[:, 0],
                             important_gb[:, 0], important_lg[:, 0]]
            filtered_list = [item for item, value in zip(important_all, similar) if value > 0]
            filtered_list.insert(0, important_model[:, 0])

            result = self.merge_rankings_with_spearman(filtered_list)
            train_res = PrettyTable()
            train_res.field_names = ['name', 'importance']
            for i in result:
                train_res.add_row(i)
            print("FINAL importance:\n", train_res)

if __name__ == '__main__':
    distill_tower = distilltower(False, True, '../../data/处理后/final.xlsx', 'data/处理后/describe.xlsx', 'distill-tower')
    distill_tower.process()
