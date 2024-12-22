CMPE540 - Courier routing

This repository is based on the paper:

**Bozanta, A., Cevik, M., Kavaklioglu, C., Kavuk, E. M., Tosun, A., Sonuc, S. B., Duranel, A., & Basar, A. (2022).**  
*"Courier routing and assignment for food delivery service using reinforcement learning."*  
Computers & Industrial Engineering, **164**, Article 107871.  
[DOI:10.1016/j.cie.2021.107871](https://doi.org/10.1016/j.cie.2021.107871)  

- **ScienceDirect Link**: [Courier Routing and Assignment for Food Delivery](https://www.sciencedirect.com/science/article/pii/S0360835221007750?casa_token=2Su7ht40cmsAAAAA:iyu9y-WqTahGbxWis69BdKhVzFtR1Y-6m-SuWFnOaWD0enQQPhKXhJXDP8XhYTadEgF4xREA__Q)

---

Recommendation from one of the authors
parametreler şöyle:  discount_factor = 0.95, alpha = 0.2, epsilon=0.1
number of episodes: 1000
Burada 5x5'li bir grid olsa bile her grid'de restoran olamayacağı için (gerçek hayatta da bu böyle) restoran olan gridleri önceden belirliyorduk. Aynı şekilde bazı yerlerde müşteri olma olasılığı daha yüksek yine o gridler de önceden belirleniyor. Tabii bu biraz da simplicity için yoksa uzay çok büyüyor. 
Ona da makaledeki figure 4'ten ulaşabilirsin.
Hyperparameter tunning yapmışız, Tablo 3'te sonuçları var.