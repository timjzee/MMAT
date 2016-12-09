library(lattice)

HNR_dataset <- read.csv("/Users/tim/Documents/sound_files/MMAT/hnr_values_norm.csv")
HNR_dataset$manipulation = factor(HNR_dataset$manipulation)

bwplot(HNR ~ manipulation, data = HNR_dataset, xlab = "Manipulation", ylab = "HNR (dB)")

HNR_model = lm(HNR ~ manipulation, data = HNR_dataset)
summary(HNR_model)
