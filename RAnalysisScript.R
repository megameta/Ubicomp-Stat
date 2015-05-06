# I can't remember what this library does. Might be for plotting the ANOVA.
library(car)
prelim_results = read.csv("D:\\Dropbox\\School\\Ubicomp\\Data Analysis\\cs7470\\Prelim_Results.csv")

prelim_results$Adv.Latency = as.factor(prelim_results$Adv.Latency)
prelim_results$Adv.Power = as.factor(prelim_results$Adv.Power)
prelim_results$Distance = as.factor(prelim_results$pos)
prelim_results$Listener.Latency = as.factor(prelim_results$Listener.Latency)

# ANOVA can be performed on all factors. See differences in type for more info.
lmANOVA = lm(Time_to_Discovery ~ Adv.Latency*pos*Adv.Power*Listener.Latency, data=prelim_results)
Anova(lmANOVA, type = "II")

# Tukey can be performed on any linear model with only one factor
lmTUKEY = lm(Time_to_Discovery ~ Adv.Power, data=prelim_results)
TukeyHSD(aov(lmTUKEY))
