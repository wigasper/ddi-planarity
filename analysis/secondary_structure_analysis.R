library(ggplot2)
library(tidyr)

data <- read.csv("helix_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="helices", columns, na.rm=TRUE)
p <- ggplot(data, aes(helices, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p

data <- read.csv("strand_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="strands", columns, na.rm=TRUE)
p <- ggplot(data, aes(strands, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p

data <- read.csv("helix_residue_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="helices", columns, na.rm=TRUE)
p <- ggplot(data, aes(helices, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p

data <- read.csv("strand_residue_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="strands", columns, na.rm=TRUE)
p <- ggplot(data, aes(strands, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p
#################################
#################################
data <- read.csv("helix_residue_prop_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="helices", columns, na.rm=TRUE)
p <- ggplot(data, aes(helices, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p

data <- read.csv("strand_residue_prop_data.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="strands", columns, na.rm=TRUE)
p <- ggplot(data, aes(strands, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p

#####################################
data <- read.csv("num_repeats_by_planarity.csv")
t.test(data$planars, data$nonplanars)

columns <- c(1,2)
data <- data %>% gather(key="planarity", value="repeats", columns, na.rm=TRUE)
p <- ggplot(data, aes(repeats, color=factor(planarity), fill=factor(planarity), alpha=.5)) + geom_density()
p
