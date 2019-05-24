import numpy as np

def TILAb_Score(prob_map, cell_size):
    # prob_map: MxNx4 numpy array contains the probabilities
    # cell_size: number of patch to be consider as one grid-cell

    pred_map = np.argmax(prob_map, axis=2)

    T = np.int8(pred_map == 2)  # patches predicted as tumour
    L = np.int8(pred_map == 3)  # patches predicted as lymphocyte

    [rows, cols] = T.shape
    stride = np.int32(cell_size / 2)

    t = np.zeros(len(range(0, rows - cell_size + 1, stride))*len(range(0, cols - cell_size + 1, stride)))
    l = np.zeros(len(range(0, rows - cell_size + 1, stride))*len(range(0, cols - cell_size + 1, stride)))
    k = 0

    # probability of tumour and lymphocytes in each grid cell
    for i in range(0, rows - cell_size + 1, stride):
        for j in range(0, cols - cell_size + 1, stride):
            t[k] = np.mean(np.mean(T[i:i + cell_size, j:j + cell_size]))
            l[k] = np.mean(np.mean(L[i:i + cell_size, j:j + cell_size]))
            k += 1

    # removing grid cells with no tumour and lymphocytes regions
    index = np.logical_and(t == 0, l == 0)
    index = np.where(index)[0]

    t = np.delete(t, index)
    l = np.delete(l, index)

    tilab_score = 0.0
    if len(t) == 0:  # ideally each WSI should have some tumour or lymphocyte region to get a sensible TILAb-score
        tilab_score = 1  # if there is no tumour then its good for patients long term survival
    else:
        # normalizaing the percentage of tumour and lymphocyte range to [0-1] in a grid-cell
        t = t/(t + l)
        l = l/(t + l)

        # Morisita-Horn Index based colocalization socre
        coloc_score = (2 * sum(t*l)) / (sum(t**2) + sum(l**2))
        if np.sum(t) == 0:
            tilab_score = 1 # when only lymphocytes are present
        else:
            l2t_ratio = np.sum(l) / np.sum(t)  # lymphocyte to tumour ratio
            tilab_score = 0.5 * coloc_score * l2t_ratio  # final TILAb-score

    return tilab_score