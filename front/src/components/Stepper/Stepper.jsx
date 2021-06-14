import { makeStyles } from "@material-ui/core/styles";
import Stepper from "@material-ui/core/Stepper";
import Step from "@material-ui/core/Step";
import StepLabel from "@material-ui/core/StepLabel";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import { useEffect, useState } from "react";
import FirstStep from "../FirstStep/FirstStep";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { GET_RECOMM } from "../../redux/types/skillTypes";
import SecondStep from "../SecondStep/SecondStep";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
  backButton: {
    marginRight: theme.spacing(1),
  },
  instructions: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
}));

function getSteps() {
  return [
    "Выбери свои ключевые навыки",
    "Отметь интересуемые вакансии",
    "Пройди тест на необходимые знания",
    "Результат",
  ];
}

function getStepContent(stepIndex) {
  switch (stepIndex) {
    case 0:
      return <FirstStep></FirstStep>;
    case 1:
      return <SecondStep></SecondStep>;
    case 2:
      return "Тестирование";
    default:
      return "Отображение результатов";
  }
}

export default function HorizontalLabelPositionBelowStepper() {
  const dispatch = useDispatch();
  const skills = useSelector((state) => state.skills);
  const classes = useStyles();
  const [activeStep, setActiveStep] = useState(0);
  const steps = getSteps();
  const choice = useSelector((state) => state.choosed);
  useEffect(() => {
    if (activeStep > 0) {
      handleNext();
    }
  }, [choice]);

  const handleNext = async () => {
    if (activeStep === 0) {
      await fetch("https://netology-career-app.herokuapp.com/best_vacancies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ skills }),
      })
        .then((response) => response.json())
        .then((response) =>
          response
            ? dispatch({ type: GET_RECOMM, payload: response.rows })
            : console.log("Failed")
        );
      // .then(dispatch());
    }
    if (activeStep === 1) {
      fetch("https://netology-career-app.herokuapp.com/best_vacancies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ skills }),
      }).then((response) => console.log(response));
    }
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  return (
    <div className={classes.root}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <div>
        {activeStep === steps.length ? (
          <div>
            <Typography className={classes.instructions}>
              Удачного обучения
            </Typography>
            <Button onClick={handleReset}>Пройти сначала</Button>
          </div>
        ) : (
          <div>
            <Typography className={classes.instructions}>
              {getStepContent(activeStep)}
            </Typography>
            <div>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
                className={classes.backButton}
              >
                Назад
              </Button>
              <Button variant="contained" color="primary" onClick={handleNext}>
                {activeStep === steps.length - 1 ? "Результат" : "Далее"}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
