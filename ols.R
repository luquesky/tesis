options(digits = 4)
options(repos="http://cran.us.r-project.org")

ap_files <- c(
  "ENG_MAX",
  "ENG_MEAN",
  "F0_MEAN",
  "F0_MAX"
  # "NOISE_TO_HARMONICS_RATIO",
  # "PHONEMES_AVG",
  # "PHONEMES_COUNT",
  # "SOUND_VOICED_LOCAL_SHIMMER",
  # "SYLLABES_AVG",
  # "SYLLABES_COUNT",
  # "VCD2TOT_FRAMES"
)


social_vars <- c(
  "bored_with_game",
  "difficult_for_partner_to_speak" ,
  "contributes_to_successful_completion",
  "engaged_in_game",
  "gives_encouragement",
  "making_self_clear",
  "planning_what_to_say",
  "dislikes_partner")



for (ap_var in ap_files) {
  path <- paste("tables/", ap_var, ".csv", sep="")
  dat <- read.csv(path)

  dat["abs_entrainment"] <- abs(dat["entrainment"])

  dev.new();
  par(mfrow=c(2,2))
  i = 1;
  while ( i <= length(social_vars)) {
    social_var <- social_vars[i]
    subdat <- dat[c("abs_entrainment", social_var)]

    plot(subdat)

    title(ap_var, outer=TRUE)
    if (i == 4) {
      dev.new()
      par(mfrow=c(2,2))
    }
    i <- i + 1
  }
}
