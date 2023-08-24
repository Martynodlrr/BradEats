import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';

import { shoppingCartReducer } from './shoppingCart';
import { restaurantReducer } from './restaurant';
import { reviewReducer } from './review';
import session from './session'

const rootReducer = combineReducers({
  session,
  restaurants: restaurantReducer,
  reviews: reviewReducer,
  shopppingCart: shoppingCartReducer
});


let enhancer;

if (process.env.NODE_ENV === 'production') {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = require('redux-logger').default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
