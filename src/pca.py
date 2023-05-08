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

def pca_plot(mission:int,file_name : str = "save-100iter-no_dup_acc.csv", feature = "SENSORY", is3D = False):
        mis = ["AAC","COVERAGE","SHELTER","HOMING"]
        title= f"{feature} - {mis[mission]} "
        AX1 = "PC1"
        AX2 = "PC2"
        AX3 = "PC3"
        pca = PCA(n_components=3)
        db = pd.read_csv(file_name)

        result = pca.fit_transform(db.iloc[:,:-4])

        result_df = pd.DataFrame(data = result
                    , columns = ['1', '2','3'])

        result_df['y'] = db['fit'].apply(lambda x: float(x.replace("[","").replace("]","").split(',')[mission]))

        cmap = ListedColormap(sns.color_palette("rocket_r").as_hex())

        if is3D:
            fig = plt.figure(figsize=(16,10))
            ax = Axes3D(fig, auto_add_to_figure=False)
            fig.add_axes(ax)


            sc = ax.scatter(result_df['1'], result_df['2'], result_df['3'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
            ax.set_xlabel(AX1)
            ax.set_ylabel(AX2)
            ax.set_zlabel(AX3)

            plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)
        else:
            fig, axs = plt.subplots(2, 2, figsize=(16, 10))

            # XY plane
            im = axs[0, 0].scatter(result_df['1'], result_df['2'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
            axs[0, 0].set_xlabel(AX1)
            axs[0, 0].set_ylabel(AX2)

            # XZ plane
            im = axs[0, 1].scatter(result_df['1'], result_df['3'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
            axs[0, 1].set_xlabel(AX1)
            axs[0, 1].set_ylabel(AX3)

            # YX plane
            im = axs[1, 0].scatter(result_df['2'], result_df['1'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
            axs[1, 0].set_xlabel(AX2)
            axs[1, 0].set_ylabel(AX1)

            # YZ plane
            im = axs[1, 1].scatter(result_df['2'], result_df['3'], s=40, c=result_df['y'], marker='o', cmap=cmap, alpha=1)
            axs[1, 1].set_xlabel(AX2)
            axs[1, 1].set_ylabel(AX3)

            # Add a giant colorbar to the right of all subplots
            fig.colorbar(im, ax=axs.ravel().tolist(), shrink=0.6)
            fig.suptitle(f'2D Scatter Plots from All Sides of 3D PCA Plot {title} ', fontsize=16)

        plt.show()

def pca_variance(file_name : str = "save-100iter-no_dup_acc.csv"):
    db = pd.read_csv(file_name)
    pca = PCA(10)
    result = pca.fit_transform(db.iloc[:,:-4])

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = [f'PC{str(x)}' for x in range(1,len(per_var)+1)]    

    plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label = labels)
    plt.ylabel('Percentage of Explained Variance')
    plt.xlabel('Principal Component')
    plt.title('Scree Plot')
    plt.show()

def loading_scores(file_name : str = "save-100iter-no_dup_acc.csv"):
    db = pd.read_csv(file_name)
    pca = PCA(10)
    result = pca.fit_transform(db.iloc[:,:-4])
    loading_score = pd.Series(pca.components_[0],index = db.columns[:-4])
    sorted_loading = loading_score.abs().sort_values(ascending=False)
    top10 = sorted_loading[:10].index.values

    print(loading_score[top10])

def get_best_pfsm(amount, file_name,output="best_pfsm.txt"):
    db = pd.read_csv(file)
    db['AAC'] = db['fit'].apply(lambda x: float(x.replace("[","").replace("]","").split(',')[0]))
    db['COVERAGE'] = db['fit'].apply(lambda x: float(x.replace("[","").replace("]","").split(',')[1]))
    db['HOMING'] = db['fit'].apply(lambda x: float(x.replace("[","").replace("]","").split(',')[2]))
    db['SHELTER'] = db['fit'].apply(lambda x: float(x.replace("[","").replace("]","").split(',')[3]))
    print(db.head())

    best_pfsm = []
    missions = ["AAC","COVERAGE","HOMING","SHELTER"]
    with open(output,"w") as f:
        for mission in missions:
            f.write(f"{mission}\n")
            best = db.nlargest(2,mission)
            pfsms = best.geno.tolist()
            best_pfsm.append(pfsms)
            for pfsm in pfsms:
                f.write(f"{pfsm}\n")
    # print(best_pfsm)

if __name__ == "__main__":
    file = "/home/laurent/Documents/Polytech/MA2/thesis/ALL_SENSORY_features.csv"
    get_best_pfsm(2,file)
    # pca_variance(file)
    # loading_scores(file)
    # pca_2d_plot()
    # pca_plot(1,file)
