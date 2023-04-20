from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


pca = PCA(n_components=2)

db = pd.read_csv("save-100iter-no_dup_acc.csv")

result = pca.fit_transform(db.iloc[:,:-3])

result_df = pd.DataFrame(data = result
             , columns = ['principal component 1', 'principal component 2'])

result_df['y'] = db['fitness']

print(result_df.head())

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(16,10))
sns.scatterplot(
    x="principal component 1", y="principal component 2",
    hue="y",
    palette=sns.color_palette("hls", 10),
    data=result_df,
    legend="full",
    alpha=0.3
)
plt.show()

pca = PCA(n_components=3)
db = pd.read_csv("save-300iter_possible-dup.csv")

result = pca.fit_transform(db.iloc[:,:-3])

result_df = pd.DataFrame(data = result
             , columns = ['1', '2','3'])

result_df['y'] = db['fitness']

print(result_df.head())

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# plt.figure(figsize=(16,10))
# sns.scatter(
#     x="principal component 1", y="principal component 2", z ="principal component 3",
#     hue="y",
#     palette=sns.color_palette("hls", 10),
#     data=result_df,
#     legend="full",
#     alpha=0.3
# )
# plt.show()

fig = plt.figure(figsize=(16,10))
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)

# get colormap from seaborn
cmap = ListedColormap(sns.color_palette("husl", 256).as_hex())

# plot
sc = ax.scatter(result_df['1'], result_df['2'], result_df['3'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# legend
plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)

# save
# plt.savefig("scatter_hue", bbox_inches='tight') 
plt.show()

db = pd.read_csv("save-300iter_possible-dup_acc.csv")

result = pca.fit_transform(db.iloc[:,:-3])

result_df = pd.DataFrame(data = result
             , columns = ['x', 'y','y'])

# result_df['w'] = db['fitness']

# fig = plt.figure(figsize=(16,10))
# sns.pairplot(result_df)
# plt.show()