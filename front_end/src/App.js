import React, { Component } from 'react';
import { BrowserRouter, Route} from 'react-router-dom';

import CameraOpen from './components/Cameraopen';
import Filter from './components/Filter';
import Suggested from './components/Suggested';
import Uploadphoto from './components/Uploadphoto';


class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      image: null,
      filter: '',
      showWarning: true,
      url_list:[]
    }

  }
  
  render(){
    return(
      <BrowserRouter>
        <div style={{height:'100%'}} className="App">

        <Route path="/" exact strict component={CameraOpen} callbackFromParent={this.Callback}/>
        {/* <Route path="/filter" component={Filter}/> */}
        {/* <Route path="/suggest" component={Suggested} Suggested={this.state.url_list}/> */}
        <Route path="/test" component={Uploadphoto}/>

        </div>
      </BrowserRouter>
    )
  }
}

export default App;