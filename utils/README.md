## Simple tool to generate a md table to send on discord for clan score weekly guidance

Relative end
```
python3 weekly_quota.py --start "2025-08-01 11:00" --end "2025-09-01 11:00" --weekly_quota 2.5,4,3,3,3  --relative_end
Week  Start                  → End                  Days  Quota  Accumulated
----------------------------------------------------------------------------
1     <t:1754060400>         <t:1754665200:R>       7     17     17m
2     <t:1754665200>         <t:1755270000:R>       7     28     45m
3     <t:1755270000>         <t:1755874800:R>       7     21     66m
4     <t:1755874800>         <t:1756479600:R>       7     21     87m
5     <t:1756479600>         <t:1756738800:R>       3     9      96m
```

Variable quota + relative_end
```
python3 weekly_quota.py --start "2025-08-01 11:00" --end "2025-09-01 11:00" --daily_quota 3 --relative_end
Week  Start                  → End                  Days  Quota  Accumulated
----------------------------------------------------------------------------
1     <t:1754060400>         <t:1754665200:R>       7     21     21m
2     <t:1754665200>         <t:1755270000:R>       7     21     42m
3     <t:1755270000>         <t:1755874800:R>       7     21     63m
4     <t:1755874800>         <t:1756479600:R>       7     21     84m
5     <t:1756479600>         <t:1756738800:R>       3     9      93m
```


Static quota
```
python3 weekly_quota.py --start "2025-08-01 11:00" --end "2025-09-01 11:00" --daily_quota 3
Week  Start                  → End                  Days  Quota  Accumulated
----------------------------------------------------------------------------
1     <t:1754060400>         <t:1754665200>         7     21     21m
2     <t:1754665200>         <t:1755270000>         7     21     42m
3     <t:1755270000>         <t:1755874800>         7     21     63m
4     <t:1755874800>         <t:1756479600>         7     21     84m
5     <t:1756479600>         <t:1756738800>         3     9      93m
```