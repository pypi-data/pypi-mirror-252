A simple dice roll probability package inspired by anydice.com. There are many like it, but this one is mine.

# Usage

Dice rolls use the `dice_roll` class. The most basic dice roll is consist of a number of dice and a number of sides. For example, to roll three six sided dice or 3d6:

```
dnd = dice_roll((3,6))
```

You can drop the lowest rolls by using the drop option. So, to get the 4d6 drop lowest D&D stat roll

```
dndDrop = dice_roll((4,6),drop=1)
print(dnd)
```

```
             pmf       cmf
domain                    
3       0.000611  0.000611
4       0.001833  0.002443
5       0.003665  0.006109
6       0.008312  0.014421
7       0.015774  0.030195
8       0.026050  0.056245
9       0.041685  0.097930
10      0.062678  0.160608
11      0.082418  0.243026
12      0.108365  0.351391
13      0.127389  0.478780
14      0.139489  0.618268
15      0.135985  0.754254
16      0.123489  0.877743
17      0.079540  0.957283
18      0.042717  1.000000
```

We can also apply a function to the dice roll afterwards. This can be done in the dice_roll constructor or with the `apply_function` method. For example, we can get the D&D stat modifier distribution

```
dndDrop_modifiers = dnd.apply_function(lambda x: (x-10)//2)
```
Note, the function is always cast to an integer.

You can plot the distribution with the `plot` method.

```
dndDrop_modifiers.plot(title="4d6 Drop Lowest Stat Modifiers")
```

![4d6 Drop Lowest Stat Modifiers Plot](https://github.com/jtrainrva/dice_roller/blob/main/dndarray_modifiers.png?raw=True)

`dice_roll` supports mean, median, and mode.

```
[dndDrop_modifiers.mean,dndDrop_modifiers.median,dndDrop_modifiers.mode]
```

```
[1.4318137860082305, 2, 2]
```

Quantiles are also availible with the `quantile` method.

```
dndDrop_modifiers.quantile([.05,.95])
```

```
array([-1,  3])
```

You can add and subtract any two dice_roll distributions.

```
dice_roll((1,6))+dice_roll((1,6))-dice_roll((2,6))
```

```
             pmf       cmf
domain                    
-10     0.000772  0.000772
-9      0.003086  0.003858
-8      0.007716  0.011574
-7      0.015432  0.027006
-6      0.027006  0.054012
-5      0.043210  0.097222
-4      0.061728  0.158951
-3      0.080247  0.239198
-2      0.096451  0.335648
-1      0.108025  0.443673
 0      0.112654  0.556327
 1      0.108025  0.664352
 2      0.096451  0.760802
 3      0.080247  0.841049
 4      0.061728  0.902778
 5      0.043210  0.945988
 6      0.027006  0.972994
 7      0.015432  0.988426
 8      0.007716  0.996142
 9      0.003086  0.999228
 10     0.000772  1.000000
```

You can compute the sum of a sample of size `k` from a dice_roll object using thr `sum` method. This supports dropping the lowest roll.

```
dndDrop.sum(6,drop=2).plot(title="D&D Stat Array Total Modifiers with Two Dump Stats")
```

![D&D Stat Array Total Modifiers with Two Dump](https://github.com/jtrainrva/dice_roller/blob/main/dndarray_modifiers_dumpstats.png?raw=True)

Lastly, you can export the table of support, pmf and cmf to a Pandas datafram with the `df` method.

```
dndDrop_modifiers.df
```
