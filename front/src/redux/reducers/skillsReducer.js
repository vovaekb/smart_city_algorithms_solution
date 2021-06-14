import { ADD_SKILL, DELETE_SKILL, GET_RECOMM, CHOOSE_RECOMM} from "../types/skillTypes";

const skillsReducer = (state, action) => {
  switch (action.type) {
    case ADD_SKILL:
      return {
        ...state,
        skills: [...state.skills, action.payload],
      };
    case DELETE_SKILL:
      return {
        ...state,
        skills: state.skills.filter((skills) => skills !== action.payload),
      };
    case GET_RECOMM:
      return {
        ...state,
        recomm: action.payload,
      };
      case CHOOSE_RECOMM:
      return {
        ...state,
        choosed: action.payload,
      };
    default:
      return state;
  }
};
export default skillsReducer;
