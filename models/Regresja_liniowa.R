library(dplyr)
library(ggplot2)

# Przygotowanie danych

data <- read.csv("NEW_clean_data.csv")

colnames(data)

data <- data[, c("runtime", "year", "quarter", "budget_adjusted", "revenue_adjusted",
                 "main_genre", "main_country", "original_language", "vote_count", "vote_average",
                 "director_avg_revenue", "writer_avg_revenue", "actors_avg_revenue",
                 "female_actors", "top_people_number")]

data <- data %>%
  mutate(original_language = ifelse(original_language == "en", "en", "other")) %>%
  add_count(main_country) %>% 
  mutate(main_country = ifelse(n >= 200, main_country, "Other")) %>%
  select(-n)
  
table(data$main_country)

data$main_country <- as.factor(data$main_country)
data$original_language<- as.factor(data$original_language)

data$main_genre <- as.factor(data$main_genre)

data$main_country <- relevel(data$main_country, ref = "USA")
data$original_language <- relevel(data$original_language, ref = "en")
data$main_genre <- relevel(data$main_genre, ref = "adventure") 

# Przygotowanie do trenowania


# Usuwanie outlierów 

dolna_granica <- quantile(data$revenue_adjusted, 0.01, na.rm = TRUE)
gorna_granica <- quantile(data$revenue_adjusted, 0.99, na.rm = TRUE)

print(paste("Usuwam filmy zarabiające poniżej:", round(dolna_granica)))
print(paste("Usuwam filmy zarabiające powyżej:", round(gorna_granica)))

data_bez_outlierow <- data %>%
  filter(revenue_adjusted >= dolna_granica & revenue_adjusted <= gorna_granica)

boxplot(data_bez_outlierow$revenue_adjusted)

# Przygotowanie zbiorów

set.seed(123)

indeksy <- sample(1:dim(data_bez_outlierow)[1], round(0.7 * dim(data_bez_outlierow)[1]), replace = FALSE)
train <- data_bez_outlierow[indeksy,]
test <- data_bez_outlierow[-indeksy,]



# Zwykły model

model <- lm(revenue_adjusted ~ ., data = train)
summary(model)

predykcje <- predict(model, newdata = test)
prawdziwe_wartosci <- test$revenue_adjusted
bledy <- prawdziwe_wartosci - predykcje

MAE <- mean(abs(bledy))
print(paste("MAE:", round(MAE, 2)))

RMSE <- sqrt(mean(bledy^2))
print(paste("RMSE:", round(RMSE, 2)))

MAPE <- mean(abs(bledy / prawdziwe_wartosci), na.rm = TRUE) * 100
print(paste("MAPE:", round(MAPE, 2), "%"))

wyniki <- data.frame(prawdziwe = test$revenue_adjusted,
                                 predykcje = predykcje)

wyniki <- wyniki %>% mutate(
  reszty = prawdziwe - predykcje)


ggplot(wyniki, aes(x = prawdziwe, y = predykcje)) +
  geom_point(alpha = 0.4, color = "darkblue") +
  geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", size = 1) +
  labs(title = "Przewidywania vs rzeczywistość",
       subtitle = "Czerwona linia oznacza model idealny",
       x = "Rzeczywisty przychód",
       y = "Przewidywany przychód") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()


ggplot(wyniki, aes(x = predykcje, y = reszty)) +
  geom_point(alpha = 0.4, color = "darkblue") +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed", size = 1) +
  labs(title = "Wykres reszt",
       x = "Przewidywany przychód",
       y = "Błąd") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()

par(mfrow = c(2, 2))
plot(model)
par(mfrow = c(1, 1))

###############################################################3

# Model krokowy

model_pelny <- lm(revenue_adjusted ~ ., data = train)
model_krokowy <- step(model_pelny, direction = "both", trace = 0)

print(formula(model_krokowy))

summary(model_krokowy)
predykcje_krokowe <- predict(model_krokowy, newdata = test)

prawdziwe_wartosci <- test$revenue_adjusted
bledy_krokowe <- prawdziwe_wartosci - predykcje_krokowe

MAE_krokowe <- mean(abs(bledy_krokowe))
print(paste("Regresja krokowa MAE: ", formatC(MAE_krokowe, format="f", big.mark=",", digits=2)))

RMSE_krokowe <- sqrt(mean(bledy_krokowe^2))
print(paste("Regresja krokowa RMSE: ", formatC(RMSE_krokowe, format="f", big.mark=",", digits=2)))

MAPE_krokowe <- mean(abs(bledy_krokowe / prawdziwe_wartosci), na.rm = TRUE) * 100
print(paste("Regresja krokowa MAPE:", round(MAPE_krokowe, 2), "%"))


wyniki_krokowe <- data.frame(prawdziwe = test$revenue_adjusted,
                     predykcje = predykcje_krokowe)

wyniki_krokowe  <- wyniki_krokowe %>% mutate(
  reszty = prawdziwe - predykcje)


ggplot(wyniki_krokowe, aes(x = prawdziwe, y = predykcje)) +
  geom_point(alpha = 0.4, color = "darkblue") +
  geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", size = 1) +
  labs(title = "Przewidywania vs rzeczywistość",
       subtitle = "Czerwona linia oznacza model idealny",
       x = "Rzeczywisty przychód",
       y = "Przewidywany przychód") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()


ggplot(wyniki_krokowe, aes(x = predykcje, y = reszty)) +
  geom_point(alpha = 0.4, color = "darkblue") +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed", size = 1) +
  labs(title = "Wykres reszt",
       x = "Przewidywany przychód",
       y = "Błąd") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal()


ggplot(wyniki_krokowe, aes(x = prawdziwe, y = predykcje)) +
  geom_point(alpha = 0.5, color = "darkblue", size = 2) +
  geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", linewidth = 1.5) +
  labs(title = "Przewidywania vs rzeczywistość",
       subtitle = "Czerwona linia oznacza model idealny",
       x = "Rzeczywisty przychód",
       y = "Przewidywany przychód") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal(base_size = 18) +
  theme(
    plot.title = element_text(size = 26, face = "bold", margin = margin(b = 10)), # Wielki, pogrubiony tytuł
    plot.subtitle = element_text(size = 18, color = "gray30", margin = margin(b = 20)),
    axis.title.x = element_text(size = 20, face = "bold", margin = margin(t = 15)), # Oś X
    axis.title.y = element_text(size = 20, face = "bold", margin = margin(r = 15)), # Oś Y
    axis.text = element_text(size = 16) # Cyfry na osiach
  )


ggplot(wyniki_krokowe, aes(x = predykcje, y = reszty)) +
  geom_point(alpha = 0.5, color = "darkblue", size = 2) +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed", linewidth = 1.5) +
  labs(title = "Wykres reszt",
       subtitle = "Odchylenia prognoz od rzeczywistości",
       x = "Przewidywany przychód",
       y = "Błąd") +
  scale_x_continuous(labels = scales::comma) + 
  scale_y_continuous(labels = scales::comma) +
  theme_minimal(base_size = 18) +
  theme(
    plot.title = element_text(size = 26, face = "bold", margin = margin(b = 10)),
    plot.subtitle = element_text(size = 18, color = "gray30", margin = margin(b = 20)),
    axis.title.x = element_text(size = 20, face = "bold", margin = margin(t = 15)),
    axis.title.y = element_text(size = 20, face = "bold", margin = margin(r = 15)),
    axis.text = element_text(size = 16)
  )

par(mfrow = c(2, 2))
plot(model_krokowy)
par(mfrow = c(1, 1))



