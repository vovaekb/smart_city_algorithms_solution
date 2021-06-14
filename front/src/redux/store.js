import {createStore} from 'redux'
import initState from './initState'
import {composeWithDevTools} from "redux-devtools-extension"
import skillsReducer from './reducers/skillsReducer'

const store = createStore(skillsReducer, initState, composeWithDevTools())

export default store
