from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def pca_2d_plot(file_name : str = "save-100iter-no_dup_acc.csv"):
    pca = PCA(n_components=2)

    db = pd.read_csv(file_name)

    result = pca.fit_transform(db.iloc[:,:-3])

    result_df = pd.DataFrame(data = result
                , columns = ['principal component 1', 'principal component 2'])

    result_df['y'] = db['fitness']

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

def pca_3d_plot(file_name : str = "save-100iter-no_dup_acc.csv"):
    pca = PCA(n_components=3)
    db = pd.read_csv(file_name)

    result = pca.fit_transform(db.iloc[:,:-3])

    result_df = pd.DataFrame(data = result
                , columns = ['1', '2','3'])

    result_df['y'] = db['fitness']

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

def pca_variance(file_name : str = "save-100iter-no_dup_acc.csv"):
    db = pd.read_csv(file_name)
    pca = PCA(10)
    result = pca.fit_transform(db.iloc[:,:-3])

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = [f'PC{str(x)}' for x in range(1,len(per_var)+1)]    

    plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label = labels)
    plt.ylabel('Percentage of Explained Variance')
    plt.xlabel('Principal Component')
    plt.t('Scree Plot')
    plt.show()

def loading_scores(file_name : str = "save-100iter-no_dup_acc.csv"):
    db = pd.read_csv(file_name)
    pca = PCA(10)
    result = pca.fit_transform(db.iloc[:,:-3])
    loading_score = pd.Series(pca.components_[0],index = db.columns[:-3])
    sorted_loading = loading_score.abs().sort_values(ascending=False)
    top10 = sorted_loading[:10].index.values

    print(loading_score[top10])


if __name__ == "__main__":
    pca_variance()
    loading_scores()
    # pca_2d_plot()
    # pca_3d_plot()
