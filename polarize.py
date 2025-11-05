import numpy as np
import sys

# ===== UTILITAIRES =====


def bit_reversal_permutation(N):
    """
    Une "bit reversal permutation" est un inversement des bits décrivant
    un nombre en binaire.
    Cette fonction renvoie une liste ordonnées des bit reversal permutation
    des  entiers de 0 à N-1.
    """

    n = int(np.log2(N))
    return np.array([int(format(i, f'0{n}b')[::-1], 2) for i in range(N)])




def kronecker_matrix(n):
    """
    Cette fonction calcule la puissance de Kronecker n-ième de la matrice 4x4
    suivante.
    [1 0]
    [1 1]

    Cela permet l'encodage, et sa transposée aide au décodage
    """
    F = np.array([[1, 0], [1, 1]], dtype=np.uint8)
    G = F
    for _ in range(n - 1):
        G = np.kron(G, F)
    return G


def kronecker_matrix_trans(n):
    F = np.array([[1, 1], [0, 1]], dtype=np.uint8)
    G = F
    for _ in range(n - 1):
        G = np.kron(G, F)
    return G
    


def construct_bec(N, epsilon) :
    """
    Cette fonction calcule  recursivement la probabilité d'effacement d'un sous-canal
    de notre polarisation.
    Elle renvoie les K indices des bits ayant la probabilité la plus faible, soit les 
    indices des bits d'information.
    """

    Z = [epsilon for i in range (N)]
    res = []

    def recursive_calculate_probs (N, Z) :
        if N == 1 :
            res.append(Z[0])
            return

        mid = N//2
        up = Z[:mid]
        down = Z[mid:]

        next = [0] * N

        for i in range (mid) :
            next[i] = up[i] + down[i] - up[i] * down[i]
            next[i+mid] = up[i] * down[i]

        recursive_calculate_probs(mid, next[:mid])
        recursive_calculate_probs(mid, next[mid:])
    
    recursive_calculate_probs(N, Z)
    return res

def get_info_indices(N, K, epsilon)  :
    res = construct_bec(N, epsilon)
    return np.argsort(res)[:K]


# ===== CODE POLAIRE :: CRC (non utilisées) =====

def crc_encode(u, poly=[1, 0, 1, 1]):
    """Calcule et ajoute le CRC à la fin du message u (division de u(x) * x^r par g(x)).
    Par défaut : CRC-3 avec poly(x) = x^3 + x + 1.
    """
    r = len(poly) - 1
    reg = [0] * r
    data = list(u) + [0] * r  # message avec r zéros à la fin

    for bit in data:
        top = reg[0]
        reg = reg[1:] + [bit]
        if top:
            reg = [r_i ^ p_i for r_i, p_i in zip(reg, poly[1:])]

    return np.concatenate([u, reg])


def crc_check(u_crc, poly=[1, 0, 1, 1]):
    """ 
    Cette fonction permet de controler le CRC
    """
    reg = [0] * (len(poly) - 1)
    for bit in u_crc:
        top = reg[0]
        reg = reg[1:] + [bit]
        if top:
            reg = [r ^ p for r, p in zip(reg, poly[1:])]
    return all(r == 0 for r in reg)




# ===== CODE POLAIRE :: ENCODAGE =====

def encode(u, N, frozen_indices):
    """
    Crée, à partir d'un message u et des indices des bits frozen, un encodage
    polaire du message u sur N bits.
    """

    G = kronecker_matrix(int(np.log2(N)))
    perm = bit_reversal_permutation(N)
    G = G[perm, :]

    x = np.zeros(N, dtype=np.uint8)
    info_idx = [i for i in range(N) if i not in frozen_indices]
    x[info_idx] = u
    print ("Message avec les frozen bits: ", x)
    res = x @ G % 2
    return res

def simulate_bec(x, epsilon):
    return [bit if np.random.rand() > epsilon else None for bit in x]



# ===== CODE POLAIRE :: DECODAGE =====
# fonctions f et g dans le cadre du canal BEC

def f(a, b):
    if a is not None and b is not None:
        return (a + b) % 2
    return None

def g(a, b, u):
    if b is not None:
        return b
    if a is not None:
        return (a + u) % 2
    return None




def sc_decode_bec(frozen_indices, received, bhatt):
    """
    Décodage du message received suivant la méthode de Successive Cancellation.
    La variable nb_err permet un projeté du risque d'erreur, mais également
    d'amélioration via un algorithme CA-SCL.
    """
    N = len(received)
    nb_err = 0

    perm = bit_reversal_permutation(N)
    llh = [received[perm[i]] for i in range(N)]
    res = [None] * N  # contient les bits décodés

    print ("llh initial : ", llh)

    def sc_decode_recursive(indice, llr):
        nonlocal nb_err
        n = len(llr)

        if n == 1:
            if indice in frozen_indices :
                res[indice] = 0
            else :
                #print ("indice de bhattacharyya du bit ", indice, " : ", bhatt[indice])
                if llr[0] is None :
                    #print("potentielle erreur ici", llr[0])
                    nb_err += 1
                    llr[0] = 0
                res[indice] = llr[0]
            #print ("TROUVE POUR LE BIT ", indice, " : ", res[indice])
            return

        # calcul de la moitié gauche des LLRs via f
        llr_left = []
        for i in range(n // 2):
            llr_left.append(f(llr[i], llr[n//2 + i]))

        # Décodage récursif de la première moitié
        sc_decode_recursive(indice, llr_left)

        # calcul de la moitié droite des LLRs via g
        llr_right = []

        if (n==2) :
            u = res[indice]
            llr_right.append(g(llr[0], llr[1], u))

        else :
            G = kronecker_matrix_trans(int(np.log2(n//2)))
            for i in range(n // 2):
                ligne_i = G[i]
                u = 0
                for j in range(n//2):
                    if ligne_i[j] == 1:
                        u += res[indice + j]
                llr_right.append(g(llr[i], llr[n//2 + i], u))

        # Décodage récursif de la seconde moitié
        sc_decode_recursive(indice + n//2, llr_right)

    sc_decode_recursive(0, llh)
    return res, nb_err


def test_sc_decode_bec (N, K, epsilon) :
    """
    Fonction de test global, synthétisant l'ensemble du processus
    et affichant chaque étape du procédé.
    """
    message = np.random.randint(0, 2, K)

    fiab = construct_bec(N, epsilon)
    
    info_indices = get_info_indices(N, K, epsilon)
    rev = bit_reversal_permutation(N)
    info_indices_br = rev[info_indices]
    frozen_indices = [i for i in range(N) if i not in info_indices]

    print ("\nMessage initial à envoyer :", message)
    print("\nindices des frozen bits :", frozen_indices)

    codeword = encode(message, N, frozen_indices)
    received = simulate_bec(codeword, epsilon)

    print("Message encodé :", codeword)

    print("\nMessage reçu :", received)
    result, nb_err = sc_decode_bec(frozen_indices, received, fiab)
    print("Message décodé :", result)

    final = [result[i] for i in np.sort(info_indices)]
    print("\nDécodage du message initial :", final)
    print("Rappel message initial :", message)

    print("\nRéussite ? ", np.array_equal(final, message))

    print("\nNombre de bits potentiels de causer des erreurs : ", nb_err)
    print("Fiabilité du moins bon canal utilisé : ", (np.sort(fiab)[K-1]))



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 CA-SCL.py N K epsilon")
        sys.exit(1)

    N = int(sys.argv[1])
    K = int(sys.argv[2])
    epsilon = float(sys.argv[3])

    test_sc_decode_bec(N, K, epsilon)
