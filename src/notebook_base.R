rm(list=ls())
options(digits = 4)
options(repos="http://cran.us.r-project.org")
library(xtable)

if (!require("plm")) install.packages("plm")
if (!require("lmtest")) install.packages("lmtest")
if (!require("sandwich")) install.packages("sandwich")
if (!require("sqldf")) install.packages("sqldf")


social_vars <- c(
    "contributes_to_successful_completion",
    "making_self_clear",
    "engaged_in_game",
    "planning_what_to_say",
    "gives_encouragement",
    "difficult_for_partner_to_speak",
    "bored_with_game",
    "dislikes_partner")

ap_vars <- c(
    "ENG_MAX",
    "ENG_MEAN",
    "F0_MEAN",
    "F0_MAX",
    "NOISE_TO_HARMONICS_RATIO",
    "PHONEMES_AVG",
    "PHONEMES_COUNT",
    "SOUND_VOICED_LOCAL_SHIMMER",
    "SYLLABES_AVG",
    "SYLLABES_COUNT",
    "VCD2TOT_FRAMES"
)


# Carga el csv en un data frame y calcula el valor
# absoluto de entrainment.

load_csv <- function(ap_var) {
  path <- paste("tables/", ap_var, ".csv", sep="")

  data_set <- read.table(path, sep = ",", header = T,
               row.names = 1)

  data_set$real_session <- factor(paste(data_set$session,
                      data_set$speaker, sep = "_"))

  data_set$abs_entrainment <- abs(data_set$entrainment)
  data_set$entrainment_neg <- ifelse(data_set$entrainment < 0, TRUE, FALSE)
  return(data_set)
}

