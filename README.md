# Plus courts chemins avec fatigue accumulée et arrêts obligatoires

Recherche de trajets de coût minimal dans un réseau où le temps de parcours d'une arête dépend
de la fatigue accumulée avant de l'emprunter, avec extension au cas de plusieurs arrêts
obligatoires imposés dans un ordre fixé.

Projet réalisé dans le cadre du cours de programmation de l'ENSAE Paris (2026).

## 1. Formalisation

Le réseau est un graphe orienté `G = (V, E)`, `|V| = n`, `|E| = m`. Chaque arête `e = (u, v)`
porte une longueur `ℓ(e) > 0` et une fatigue `f(e) ≥ 0`.

Pour un chemin `P = (e₁, …, e_k)` parti avec une fatigue initiale `F₀`, on pose
`F_i = F_{i−1} + f(e_i)` et le coût total s'écrit

```
C(P, F₀) = Σ_{i=1..k} (1 + F_{i−1}) · ℓ(e_i)
```

Le coût d'une arête n'est donc pas une fonction de l'arête seule : il dépend de l'historique du
trajet. Dijkstra, qui suppose des poids fixés par l'arête, ne s'applique pas directement.

Deux propriétés portent tout le reste du projet :

**(P1) Monotonie.** `C(P, F₀)` est strictement croissante en `F₀`, et la fatigue accumulée ne
décroît jamais. Arriver quelque part plus fatigué ne peut jamais aider.

**(P2) Structure affine.** En développant `F_{i−1} = F₀ + Σ_{j<i} f(e_j)` :

```
C(P, F₀) = C(P, 0) + F₀ · L(P)      où L(P) = Σ ℓ(e_i)
```

Le coût d'un chemin fixé est une fonction **affine** de la fatigue d'entrée, de pente sa
longueur brute. Cette identité sert à la fois à justifier les heuristiques et à comprendre
pourquoi le problème multi-arrêts ne se décompose pas.

## 2. Plus court chemin simple : graphe étendu

### 2.1 Construction

On rend le coût markovien en intégrant la fatigue à l'état : un nœud devient un couple `(u, F)`.
Une arête `(u, F) → (v, F + f(u,v))` reçoit alors le poids **constant**
`(1 + F) · ℓ(u,v) ≥ 0`, et Dijkstra redevient légitime.

**Correction.** L'application qui à un chemin de `G` partant de `v_s` associe la suite des états
`(u_i, F_i)` est une bijection sur les chemins du graphe étendu issus de `(v_s, 0)`, et elle
préserve le coût terme à terme. Minimiser dans l'un revient exactement à minimiser dans l'autre.

**Finitude de l'espace d'états.** Un chemin optimal est nécessairement simple : par (P1), tout
cycle ajoute un temps strictement positif *et* de la fatigue, donc le supprimer donne un chemin
au moins aussi bon. Un chemin simple a au plus `n − 1` arêtes, d'où

```
F_max = (n − 1) · max_e f(e)
```

et les états `(u, F)` avec `F > F_max` ne sont jamais atteints sur un chemin optimal.

**Condition d'arrêt.** La fatigue d'arrivée n'est pas connue a priori : la cible n'est pas un
état mais un ensemble d'états `{(v_t, F) : F ≥ 0}`. D'où le paramètre `is_target`, prédicat sur
l'état plutôt qu'égalité à un nœud fixé. Sur un objectif unique, le premier `(v_t, ·)` extrait
du tas est optimal et l'on peut s'arrêter là.

### 2.2 GraphImplicit

Matérialiser tous les `(u, F)` pour `F ∈ [0, F_max]` coûte `O(n · F_max)` nœuds et
`O(m · F_max)` arêtes, alors que l'immense majorité de ces états n'est jamais atteinte — `F` ne
prend que les valeurs réalisables comme sommes de fatigues d'arêtes le long d'un chemin vers
`u`. `GraphImplicit` hérite de `Graph` et ne redéfinit que le voisinage : les successeurs de
`(u, F)` sont engendrés à la volée depuis la liste d'adjacence du graphe d'origine.

|                     | Graphe étendu explicite | `GraphImplicit`         |
| ------------------- | ----------------------- | ----------------------- |
| Nœuds créés         | tous les `(u, F)`       | seulement les atteints  |
| Arêtes stockées     | `O(m · F_max)`          | aucune                  |
| Mémoire             | `O(n · F_max)`          | `O(états visités)`      |
| Coût d'un voisinage | lecture de dictionnaire | reconstruction du tuple |

Le compromis est un surcoût constant par expansion contre une consommation mémoire pilotée par
l'exploration réelle. `GraphImplicit` perd son intérêt dans le cas dégénéré où presque tous les
états sont atteints (fatigues très petites, graphe dense), où recalculer les voisins coûte plus
cher qu'une lecture.

**Complexité.** Avec un tas binaire, `O((N + M) log N)` où `N` et `M` sont les nombres d'états et
de transitions effectivement explorés, majorés par `n · F_max` et `m · F_max`. La complexité est
donc **pseudo-polynomiale** : elle dépend de la valeur numérique des fatigues, pas seulement de
la taille du graphe. C'est ce qui rend l'élagage indispensable sur `large-largefatigue`.

## 3. Pareto pruning

### 3.1 Règle

Un état `(v, F)` atteint au temps `t` est **dominé** s'il existe un `(v, F′)` déjà atteint au
temps `t′` avec `t′ ≤ t` et `F′ ≤ F`, l'inégalité étant stricte sur au moins une composante. On
maintient `pareto : sommet → liste des couples (temps, fatigue) non dominés`.

### 3.2 Correction

Soit `S` un suffixe quelconque depuis `v`. Par (P2), le coût total d'un préfixe `(t, F)` suivi de
`S` vaut `t + C(S, 0) + F · L(S)`, expression croissante en `t` et en `F`. Donc `t′ ≤ t` et
`F′ ≤ F` impliquent que le préfixe dominant est au moins aussi bon **pour tout suffixe**. Élaguer
un état dominé ne peut pas faire perdre l'optimum : il en reste toujours un de coût inférieur ou
égal.

Deux remarques :

- Il ne suffit **pas** de conserver séparément le minimum en temps et le minimum en fatigue. Les
  deux critères ne sont pas séparables : le bon compromis dépend de `L(S)`, inconnu au moment de
  l'élagage. C'est précisément l'ensemble des non-dominés qu'il faut garder.
- Le pruning ne change ni le résultat ni la complexité dans le pire cas — le front de Pareto en
  un sommet peut compter jusqu'à `F_max + 1` points, un par valeur de fatigue atteignable. Il
  change en revanche radicalement le comportement pratique, la plupart des états intermédiaires
  étant dominés.

**Ordre des opérations.** Le test de dominance doit être fait *avant* la mise à jour de `d[u]` et
des prédécesseurs, sous peine de laisser des distances associées à des états ensuite écartés.

## 4. A\*

A\* trie la file de priorité sur `f(x) = g(x) + h(x)` au lieu de `g(x)`, ce qui oriente
l'exploration vers la cible ; Dijkstra en est le cas `h ≡ 0`. L'heuristique doit être
**admissible** — `h(x) ≤ h*(x)`, le vrai coût restant — faute de quoi on peut extraire la cible
avant d'avoir stabilisé son optimum.

### Heuristique 1 — relaxation sans fatigue

`h₁(u, F) = d_G(u, v_t)`, distance minimale dans le graphe d'origine avec les seuls poids `ℓ`,
fatigue ignorée.

- **Admissibilité** : tout chemin réel de `u` à `v_t` coûte
  `Σ (1 + F_i) ℓ_i ≥ Σ ℓ_i ≥ d_G(u, v_t)`.
- **Consistance** : pour une transition `(u, F) → (v, F+f)` de poids `w = (1 + F) ℓ(u,v)`,
  `h₁(u,F) − h₁(v,F+f) = d_G(u,v_t) − d_G(v,v_t) ≤ ℓ(u,v) ≤ w` par inégalité triangulaire.
  L'heuristique est donc consistante, et pas seulement admissible : aucun état n'a besoin d'être
  rouvert, A\* se comporte comme Dijkstra sur les coûts réduits.
- **Coût** : un unique Dijkstra à rebours depuis `v_t` sur le graphe inversé,
  `O((n + m) log n)`, négligeable. Mais elle est indifférente à `F`, donc d'autant plus lâche que
  la fatigue est élevée.

### Heuristique 2 — fatigue gelée

`h₂(u, F)` = plus court chemin de `u` à `v_t` calculé en **figeant** la fatigue à sa valeur `F`
d'arrivée en `u`, c'est-à-dire avec les poids `(1 + F) ℓ(e)`.

- **Admissibilité** : sur le trajet restant la fatigue réelle vaut `F` plus une accumulation
  positive, donc `≥ F` à chaque arête : chaque arête est sous-facturée, `h₂ ≤ h*`. Le point
  subtil est que la fatigue gelée n'est pas `0` mais celle d'arrivée en `u` — ce qui reste un
  minorant justement parce que la fatigue est croissante le long du suffixe.
- Elle domine `h₁` dès que `F > 0` et intègre l'état de fatigue courant, que `h₁` ignore.
- **Coût** : dans le cas général, un Dijkstra à rebours par valeur de `F` rencontrée, ce qui est
  lourd en précalcul.

Sans oracle sur la fatigue effectivement accumulée sur le suffixe, c'est le meilleur compromis
accessible : l'heuristique parfaite reviendrait à résoudre le problème lui-même.

## 5. Arrêts obligatoires (multi-missions)

C'est la partie la plus intéressante du projet, et celle où l'intuition « on découpe en
sous-trajets » tombe en panne.

### 5.1 Le problème

On impose une suite d'étapes `w₀ → w₁ → … → w_k` à parcourir **dans cet ordre** ; missions
successives et trajets inter-missions se ramènent tous à cette forme. La fatigue **n'est pas
remise à zéro** aux étapes : elle s'accumule sur l'intégralité du parcours, trajets
inter-missions compris. On minimise le temps total.

### 5.2 Pourquoi l'approche naïve échoue

Enchaîner `k` appels indépendants à `shortest_path` optimise chaque segment isolément. Or le
choix fait sur le segment `j` produit une fatigue de sortie qui devient le coefficient
multiplicatif de **tout ce qui suit**. Contre-exemple minimal, sur le premier segment :

| Chemin | temps | fatigue de sortie |
| ------ | ----- | ----------------- |
| A      | 10    | 100               |
| B      | 12    | 5                 |

La minimisation locale retient A (10 < 12). Mais par (P2), le reste du parcours coûte
`C(S, 0) + F · L(S)` : le surcoût de A sur la suite vaut `(100 − 5) · L(S) = 95 · L(S)` pour
2 unités de temps gagnées immédiatement. Dès que `L(S) > 2/95`, B est globalement meilleur.

Le principe d'optimalité de Bellman n'est pas violé — il ne s'applique simplement pas au seul
critère « temps ». Il vaut sur l'**état complet** `(sommet, temps, fatigue)`, ce qui impose de
propager plus d'une valeur par étape.

### 5.3 Propagation du front de Pareto

On note `Φ_j` l'ensemble des couples `(temps, fatigue)` non dominés réalisables à l'étape `w_j`.

```
Φ₀ = {(0, 0)}
Φ_{j+1} = ND( { (t + c, F + φ) : (t, F) ∈ Φ_j,
                (c, φ) = coût et fatigue d'un chemin w_j → w_{j+1} emprunté avec la fatigue F } )
```

où `ND(·)` retire les couples dominés. La réponse finale est `min { t : (t, F) ∈ Φ_k }`.

**Correction (argument d'échange).** Soit un parcours global optimal et `(t, F)` son état à
l'étape `w_j`. Si `(t, F)` était dominé par un `(t′, F′)` réalisable, remplacer le préfixe par
celui réalisant `(t′, F′)` en gardant le même suffixe `S` donnerait
`t′ + C(S,0) + F′·L(S) ≤ t + C(S,0) + F·L(S)`. La substitution est licite parce que les deux
préfixes se terminent au même sommet `w_j` et que le suffixe ne dépend du passé que par `(t, F)`.
Il existe donc toujours un optimum dont tous les états intermédiaires sont non dominés :
les conserver tous suffit, et aucun autre n'est nécessaire.

**Ce qui change dans l'appel à Dijkstra.** Sur un objectif unique on s'arrête à la première
extraction d'un `(w_{j+1}, ·)`. Ici il faut au contraire **poursuivre l'exploration** pour
récupérer tous les arrivages non dominés à l'étape : le premier extrait est le meilleur en temps,
pas nécessairement le meilleur en fatigue, et c'est peut-être ce dernier qui sauve la suite. Le
dictionnaire `pareto` déjà maintenu pour l'élagage contient exactement l'information voulue —
son entrée pour `w_{j+1}` *est* le front `Φ_{j+1}`. Le même mécanisme sert donc à deux fins
opposées : sur un trajet simple, à **jeter** des états pour aller plus vite ; ici, à en
**conserver** plusieurs pour rester optimal.

**Taille du front et complexité.** Un front en un sommet contient au plus un point par valeur de
fatigue atteignable, soit `|Φ_j| ≤ F_max + 1 = (n−1)·max f + 1` — borne pseudo-polynomiale, très
pessimiste en pratique, la dominance écrasant la majorité des candidats. Le coût total est celui
de `Σ_j |Φ_j|` explorations du graphe étendu, soit `O( k · max_j |Φ_j| · (N + M) log N )`.

**A\* et multi-étapes.** L'heuristique ne peut plus viser le terminus : elle doit minorer le coût
restant jusqu'à l'**étape courante**. Un potentiel valide pour `w_k` n'est pas admissible pour un
sous-objectif intermédiaire. On recalcule donc un Dijkstra inverse par étape, ce qui s'amortit
d'autant moins bien que les segments sont nombreux et courts.

## 6. Résultats expérimentaux

Sur `medium-smallfatigue.txt`, les quatre combinaisons pruning × A\* renvoient la même distance
optimale (**29 934**) : ni l'élagage ni l'heuristique n'altèrent la correction, seulement la
vitesse. Sur ce fichier, le surcoût de l'heuristique annule à peu près son bénéfice — le graphe
est assez petit pour que Dijkstra n'explore pas beaucoup d'inutile.

Sur `large-smallfatigue.txt`, distance optimale **2 000 993** :

| Configuration                 | États élagués | Temps    |
| ----------------------------- | ------------- | -------- |
| sans pruning                  | —             | timeout  |
| pruning seul                  | 558 048       | 21,42 s  |
| pruning + A\* (heuristique 2) | 410 710       | 17,69 s  |

Le pruning devient indispensable, et A\* apporte un gain net (~17 %) : sur un graphe étendu de
cette taille, l'heuristique élimine assez d'exploration pour amortir largement son coût. Sur
`large-largefatigue.txt`, `F_max` explose et la version sans élagage ne termine pas —
illustration directe du caractère pseudo-polynomial de la complexité.

S'il fallait ne garder qu'une des deux améliorations, ce serait le pruning : A\* réduit un
facteur constant d'exploration, le pruning attaque la dimension `F_max` elle-même, qui est ce qui
rend le problème intraitable.

## 7. Limites et prolongements

- **Enveloppe inférieure par segment.** Par (P2), chaque chemin d'un segment est caractérisé par
  le triplet `(C(P,0), L(P), fatigue totale)` et son coût vu de l'amont est la droite
  `F ↦ C(P,0) + F · L(P)`. Le chemin optimal d'un segment, en fonction de la fatigue d'entrée,
  est donc l'enveloppe inférieure d'une famille de droites : une fonction linéaire par morceaux,
  à pentes décroissantes, avec au plus autant de morceaux que de chemins non dominés. La calculer
  une fois par segment remplacerait les explorations répétées, une par point du front. La
  structure est là, elle n'est pas exploitée dans cette version.
- **Fatigues réelles.** Tout repose sur des fatigues entières pour borner l'espace d'états. Avec
  des fatigues continues, le graphe étendu s'effondre et il faudrait une formulation par états
  dominés purement continue.
- **Ordre des étapes libre.** Les arrêts sont ici imposés dans un ordre fixé. Laisser l'ordre
  libre ajoute une couche de voyageur de commerce et fait basculer le problème dans le
  NP-difficile.

## Utilisation

```python
from graph import Graph, GraphImplicit

g = GraphImplicit.from_file("data/reseau.txt")

# trajet simple
chemin, distance = g.shortest_path(vs, vt, pruning=True, heuristique=h)

# arrêts obligatoires
chemin, distance = g.multi_missions([w0, w1, w2], pruning=True)
```

Signature principale :

```python
shortest_path(self, vs, vt, is_target=None, pruning=False, heuristique=None)
```

- `is_target` : prédicat sur l'état, pour ne tester que la composante sommet quand la fatigue
  d'arrivée est inconnue. Par défaut, égalité avec `vt`.
- `pruning` : active l'élagage de Pareto ; laissé optionnel pour les comparaisons.
- `heuristique` : fonction `h(état) → minorant du coût restant`. `None` donne `h ≡ 0`, donc
  Dijkstra.

Un compteur d'états élagués est exposé pour les mesures.

## Organisation du dépôt

```
graph.py        classes Graph et GraphImplicit, shortest_path (Dijkstra / A* / pruning)
heuristics.py   précalcul des heuristiques admissibles
missions.py     arrêts obligatoires par propagation de fronts de Pareto
benchmarks.py   mesures de temps et d'états élagués
rapport.pdf     rapport détaillé
```

Les jeux de données de test ne sont pas inclus dans ce dépôt.

## Auteurs

Quentin Nosmas et Maxime — ENSAE Paris, 2026.
