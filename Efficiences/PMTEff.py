from statistics import mean
#U238 chain
EffPa234 = [0.000246093, 0, 0.000722109, 0.000121065, 0.000120861, 0.000122489, 0.000477213, 0.000241663, 0.000483033, 0.00012127, 0.000359842, 0.000243250, 0.000243576, 0.000358423, 0.000122309, 0.000357782, 0.000606796, 0.000725953, 0.000242542, 0.000244738, 0.000358938, 0, 0.000243873, 0.000242689, 0.000365097, 0.000483851, 0.000243843, 0.000364343, 0.000493583, 0.000122399, 0.000242925, 0.000489956, 0.000239894, 0.000843069, 0.000484672, 0.000362450, 0.000492126, 0.000361054, 0.000120627, 0.000121448]
EffPb214 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EffBi214 = [0.00274154, 0.00379867, 0.00276533, 0.00409992, 0.00332636, 0.00265806, 0.00301318, 0.00301117, 0.00382848, 0.00275665, 0.00351845, 0.00339943, 0.00341880, 0.00459110, 0.00283527, 0.00292012, 0.00285796, 0.00341297, 0.00285442, 0.00354984, 0.00248756, 0.00368864, 0.00247950, 0.00343446, 0.00372422, 0.00331659, 0.00298853, 0.00351979, 0.00321817, 0.00302400, 0.00356205, 0.00374777, 0.00383840, 0.00326327, 0.00363567, 0.00397126, 0.00460785, 0.00376612, 0.00322092, 0.00355838]
EffBi210 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EffTl210 = [0.00987379, 0.00963275, 0.0102832, 0.0107575, 0.0106740, 0.00886935, 0.0108655, 0.0100784, 0.0102313, #error for #09.root file
0.0109183, 0.0109318, 0.00981267, 0.0101835, 0.00876273, 0.00833768, 0.0105757, 0.0109061, 0.0110986, 0.00943605, 0.0104958, 0.00838135, 0.0108206, 0.00875371, 0.00909701, 0.00977923, 0.00995764, 0.00941299, 0.00996852, 0.00834389, 0.00837947, 0.00898426, 0.00954283, 0.0105801, 0.00896258, 0.00747608, 0.0101215, 0.00896258, 0.0104105, 0.00987159]
EffAc228 = [0, 0.000141824, 0.000144383, 0, 0, 0.000144300, 0, 0, 
EffK40 = [0, 0.00013637, 0.000271076, 0.000132732, 0, 0, 0.000136258, 0, 0.000137099, 0.000134156, 0, 0, 0, 0, 0.000134553, 0, 0.000268673, 0.000133618, 0, 0, 0.000134735, 0, 0, 0.000133422, 0, 0, 0.000133779, 0.000134264, 0.000273224, 0, 0, 0, 0.000274123, 0, 0, 0, 0, 0.000403388, 0, 0]
print('Efficiences for PMT')
print('Mean Efficiency of Pa234 ' % mean(EffPa234)))
print('Mean Efficiency of Pb214 ' + str(mean(EffPb214)))
print('Mean Efficiency of Bi214 ' + str(mean(EffBi214)))
print('Mean Efficiency of Bi210 ' + str(mean(EffBi210)))
print('Mean Efficiency of Tl210 ' + str(mean(EffTl210)))
print('Mean Efficiency of K40 ' + str(mean(EffK40)))