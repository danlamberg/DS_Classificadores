# -*- coding: utf-8 -*-
"""Atividade_Classificadores

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cXbPRpbJ-0XWLrzlNuKZS5s7n9FOIJw0

Data Science - NA_ (Not) _UP-OSO_POSITIVO Aluno: Daniel de Oliveira Lamberg

Atividade prática - classificadores
Treine uma árvore de decisão (DescisionTree) a partir da base Breast Cancer

Passos:
1. Normalizar a base. Atenção: Não é ncessário normalizar a coluna Diagnosis
2. Treinar o modelo tree
3. Salvar o modelo
4. Gerar a matriz de confusão
5. Calcular a taxa de erro e a taxa de acertos

Conectando ao Google Drive:
"""

from google.colab import drive
drive.mount('/content/drive')

"""Importação da biblioteca pandas, leitura do conjunto de dados, avaliação da frequência das classes e visualização das primeiras linhas do conjunto de dados:"""

import pandas as pd
dados = pd.read_csv('/content/drive/MyDrive/BSI/01_DATA SCIENCE/COLAB/Avaliação prática 3 - Classificadores/breast-cancer.csv', sep=';')
print('Frequência das classes')
print(dados.Class.value_counts())
dados.head()

"""Importação do SMOTE, segmentação dos dados em atributos e classes, normalização dos dados e exibição dos primeiros dados:"""

from imblearn.over_sampling import SMOTE
dados.classes = dados['Class']
dados.atributos = dados.drop(columns = ['Class'])

dados.atributos_normalizados = pd.get_dummies(dados.atributos)
rotulos_normalizados = dados.atributos_normalizados.columns
print(dados.atributos.head())

"""Criação do objeto SMOTE, aplicação do SMOTE para equilibrar as classes e
impressão dos atributos normalizados:
"""

resampler = SMOTE()
dados.atributos_b, dados.classes_b = resampler.fit_resample(dados.atributos_normalizados, dados.classes)
print(dados.atributos_normalizados)

"""Importação de bibliotecas, instanciação de um classificador de árvore de decisão, divisão dos dados em conjuntos de treinamento e teste e impressão das classes de treinamento:"""

from pprint import pprint
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier()
atr_train, atr_test, class_train, class_test = train_test_split(dados.atributos_normalizados, dados.classes, test_size=0.3)
print(class_train)

"""Treinando o modelo:"""

breast_cancer_tree = tree.fit(atr_train, class_train)

"""Fazendo previsões no conjunto de teste e avaliando a acurácia do modelo no conjunto de teste:"""

predicoes = breast_cancer_tree.predict(atr_test)

acuracia = breast_cancer_tree.score(atr_test, class_test)
print(f'Acurácia do modelo no conjunto de teste: {acuracia}')

"""Previsões no conjunto de teste usando o modelo treinado:"""

Class_predict = breast_cancer_tree.predict(atr_test)
print(Class_predict)

"""Importação de bibliotecas, cálculo da matriz de confusão, criação do objeto ConfusionMatrixDisplay, plotagem da matriz de confusão e exibição do gráfico:"""

#Matriz de contigência
import matplotlib.pyplot as plt
import sklearn
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(class_test, Class_predict)


disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = breast_cancer_tree.classes_)
disp.plot()
plt.show()

"""Visualizando resultados por outro método: Área sob a curva ROC (ROC-AUC): É uma métrica comum para avaliar modelos de classificação binária.Curva ROC:
A curva ROC pode ser plotada para visualizar a taxa de verdadeiros positivos em relação à taxa de falsos positivos em diferentes limiares de decisão.
"""

from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score

# Converter rótulos de classe em formato binário
class_test_bin = label_binarize(class_test, classes=breast_cancer_tree.classes_)
Class_predict_bin = label_binarize(Class_predict, classes=breast_cancer_tree.classes_)

# Calcular a área sob a curva ROC
auc = roc_auc_score(class_test_bin, Class_predict_bin, average='macro')
print(f'Área sob a curva ROC: {auc}')

from sklearn.metrics import roc_curve, auc

# Binarizar rótulos de classe
class_test_bin = label_binarize(class_test, classes=breast_cancer_tree.classes_)
Class_predict_bin = label_binarize(Class_predict, classes=breast_cancer_tree.classes_)

# Calcular a curva ROC para cada classe
fpr, tpr, _ = roc_curve(class_test_bin.ravel(), Class_predict_bin.ravel())
roc_auc = auc(fpr, tpr)

# Plotar a curva ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'Curva ROC (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Aleatório')
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC')
plt.legend()
plt.show()