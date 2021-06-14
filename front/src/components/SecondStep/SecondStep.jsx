import { Button, Checkbox, Chip } from "@material-ui/core";
import { useDispatch, useSelector } from "react-redux";
import { CHOOSE_RECOMM } from "../../redux/types/skillTypes";

const SecondStep = () => {
  const recomm = useSelector((state) => state.recomm);
  const dispatch = useDispatch()
  const handlerTarget = (e) => {
    e.preventDefault();
    dispatch({type: CHOOSE_RECOMM, payload: e.target.innerText})
  };

  return (
    <>
      {recomm.map((data) => {
        return (
          <Button onClick={handlerTarget}>
            {data.name} | {data.score}
          </Button>
        );
      })}{" "}
    </>
  );
};

export default SecondStep;
