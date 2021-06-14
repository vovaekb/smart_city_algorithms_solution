import { Button, FormControl, Input, InputLabel } from "@material-ui/core";
import Chip from "@material-ui/core/Chip";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { ADD_SKILL, DELETE_SKILL } from "../../redux/types/skillTypes";
import React  from 'react';


const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    listStyle: "none",
    padding: theme.spacing(0.5),
    margin: 0,
  },
  chip: {
    margin: theme.spacing(0.5),
  },
}));

const FirstStep = () => {
  const [input, setInput] = useState();

  const classes = useStyles();
  const dispatch = useDispatch();
  const [chipData, setChipData] = useState([
    { key: 0, label: "JavaScript" },
    { key: 1, label: "HTML" },
    { key: 2, label: "CSS" },
  ]);

  const handleDelete = (chipToDelete) => () => {
    setChipData((chips) =>
      chips.filter((chip) => chip.key !== chipToDelete.key)
    );
    dispatch({
      type: DELETE_SKILL,
      payload: chipToDelete.label
    })
  };

  const addHandler = (e) => {
    e.preventDefault();
    setChipData((prev) => {
      return [
        ...prev,
        {
          key: Date.now(),
          label: input,
        },
      ];
    });
    dispatch({
      type: ADD_SKILL,
      payload: input,
    })
    setInput("");
  };

  const inputSkillHandler = (e) => {
    setInput(e.target.value);
  };

  return (
    <div>
      <Paper component="ul" className={classes.root}>
        <FormControl>
          <InputLabel htmlFor="my-input">Введи навык</InputLabel>
          <Input
            id="my-input"
            value={input}
            onChange={inputSkillHandler}
            aria-describedby="my-helper-text"
          />
          <Button onClick={addHandler}>Добавить</Button>
        </FormControl>
        {chipData.map((data) => {
          return (
            <li key={data.key}>
              <Chip
                label={data.label}
                onDelete={handleDelete(data)}
                className={classes.chip}
              />
            </li>
          );
        })}
      </Paper>
    </div>
  );
};

export default FirstStep;
