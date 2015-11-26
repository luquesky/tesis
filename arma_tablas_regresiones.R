rm(list=ls())
options(digits = 4)
options(repos="http://cran.us.r-project.org")

if (!require("plm")) install.packages("plm")
if (!require("lmtest")) install.packages("lmtest")
if (!require("sandwich")) install.packages("sandwich")
if (!require("sqldf")) install.packages("sqldf")

load_csv <- function(archivo) {
  # Carga el csv en un data frame y calcula el valor
  # absoluto de entrainment.
  data_set <- read.table(archivo, sep = ",", header = T,
               row.names = 1)

  data_set$real_session <- factor(paste(data_set$session,
                      data_set$speaker, sep = "_"))

  # Pega datos del puntaje
  data_scores <- read.table("scores_table.txt", sep = "\t", header = T)
  data_set <- sqldf("SELECT ds.*, sc.score, sc.describer
             FROM data_set AS ds
             LEFT JOIN data_scores AS sc ON ds.task = sc.task AND ds.session = sc.session")

  data_set$abs_entrainment <- abs(data_set$entrainment)
  data_set$entrainment_neg <- ifelse(data_set$entrainment < 0, TRUE, FALSE)
  data_set$is_describer <- (data_set$speaker==0 & data_set$describer=="A") | (data_set$speaker==1 & data_set$describer=="B")
  return(data_set)
}

arma_tabla_regs <- function(data_set, dep) {
  # Arma una tabla con las regresiones por filas

  social_vars <- c(
    "contributes_to_successful_completion",
    "making_self_clear",
    "engaged_in_game",
    "planning_what_to_say",
    "gives_encouragement",
    "difficult_for_partner_to_speak",
    "bored_with_game",
    "dislikes_partner")

  tabla_regresiones <- data.frame()
  for (sv in social_vars) {

    formula_reg <- as.formula(paste(paste(sv, dep, sep = " ~ "), "", sep = "")) # Acá definimos la relación etre variable social y entr (puede ser absoluto) que va a tester la regresión
    regresion <- plm(formula_reg, data = data_set,
             model = "within",
             #effect = "individual",
             index=c("real_session", "task"))
    print(sv)
    # Para que el test sea igual a STATA (http://www.richard-bluhm.com/clustered-ses-in-r-and-stata-2/)
    #G <- length(unique(data_set$real_session))
    #N <- length(data_set$real_session)
    #dfa <- (G/(G - 1)) * ((N - 1)/regresion$df.residual)
    #salida <- coeftest(regresion, vcov = dfa * vcovHC(regresion, type="HC0", cluster="group", adjust = TRUE))
    salida <- coeftest(regresion, vcov=vcovHC(regresion,type="HC0",cluster="group")) # Fuente: http://stats.stackexchange.com/questions/10017/standard-error-clustering-in-r-either-manually-or-in-plm
    print(salida)
    tabla_regresiones <- rbind(tabla_regresiones, t(data.frame(as.numeric(salida))))
  }
  rownames(tabla_regresiones) <- social_vars
  colnames(tabla_regresiones) <- c("Estimate", "Std. Error", "t value", "Pr(>|t|)")
  return(tabla_regresiones)
}

vars_acusticas <- c("ENG_MAX.csv",
          "ENG_MEAN.csv",
          "F0_MAX.csv",
          "F0_MEAN.csv",
          "NOISE_TO_HARMONICS_RATIO.csv",
          "PHONEMES_AVG.csv",
          "PHONEMES_COUNT.csv",
          "SOUND_VOICED_LOCAL_SHIMMER.csv",
          "SYLLABES_AVG.csv",
          "SYLLABES_COUNT.csv",
          "VCD2TOT_FRAMES.csv")

# Loop principal para calcular las tablas
tablas_regresiones <- list()
tablas_regresiones_abs <- list()

for (v in vars_acusticas) {
  print(v)
  #tablas_regresiones[[v]]    <- arma_tabla_regs(carga_csv(v), "entrainment")
  file_path <- paste("tables/", v, sep="")
  tablas_regresiones_abs[[v]] <- arma_tabla_regs(load_csv(file_path), "abs_entrainment")
}

#capture.output(print(tablas_regresiones), file = "tablas_regresiones.txt")
capture.output(print(tablas_regresiones_abs), file = "tablas_regresiones_abs.txt")
