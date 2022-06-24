library(dplyr)
library(purrr)
library(gmodels)
# nastavenie cisiel aby zobrazovalo cele a nie exponenty
options("scipen" = 10)
data <- read.csv("covid_vaccination_vs_death_ratio.csv", sep=",")

# opis datasetu
str(data)
summary(data)

#pocet krajin
krajiny <- data$country
uni_krajiny <- unique(krajiny)
length(uni_krajiny)


# kontrola ci obsahuje nejake prazdne hodnoty
sapply(data, function(x) sum(is.na(x)))

# zbavime sa hodnot kde je pomer zaockovania nad 100%
data <- data[!(data$New_deaths < 0 | data$ratio > 100),]

# identifikacia outlierov
boxplot(data$ratio,
        ylab = "%", xlab="Pomer vakcínovanej časti populácie"
)

boxplot(data$New_deaths,
        ylab = "Počet", xlab="Prírastok na úmrtiach v daný deň"
)

#vytvorime si linearny model s predikatom ratio
model <- lm(New_deaths ~ ratio, data = data)

#pozrieme sa na vlastnosti modelu
summary(model)

#rozdelme si data podla krajin
by_country <- split(data, data$country)

#vytvorme si linearny model pre kazdu krajinu
models <- lapply(by_country, function(data) lm(New_deaths ~ ratio, data = data))
vapply(models, function(x) coef(x)[[2]], double(1))

###overme si presnost nasho modelu cross validaciou###

#vytvorme si najprv 100 subsetov ktore budu pozostavat z 50% zdrojovych dat
cross_data <- map(1:100, ~ data[sort(sample(1:dim(data)[1], size = 0.5*dim(data)[1])),])


#fitnime linearny model na kazdu vzorku teda na kazdy subset
cross_models <- map(cross_data, ~ lm(.x$New_deaths ~ .x$ratio))


####vyseparujme si beta koeficient a residualy pre kazdy model####
listfunkcii <- list(coefficients = coef, residuals = residuals)
f <- function(x) {sapply(listfunkcii, function(g) g(x))}
extractedData <- map(cross_models, ~ f(.x))

#vypocet standardnej odchylky intercept a slop values
sd(map_dbl(cross_models, ~ coef(.x)[1]))
sd(map_dbl(cross_models, ~ coef(.x)[2]))

#vypocet standardnej chybovosti RSS a RMSE pre kazdy model
rss <- map_dbl(cross_models, ~ sum(resid(.x)^2))
rse <- map_dbl(rss, ~ sqrt(.x/(0.5*dim(data)[1]-2)))
boxplot(rss, xlab = "RSS")
boxplot(rse, xlab = "RMSE")
