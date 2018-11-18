import React, { Component } from 'react';
import Camera from 'react-camera';
import {Link} from 'react-router-dom';
import {Button, Card, CardImg, CardText, CardBody,
  CardTitle, CardSubtitle} from 'reactstrap';
import axios from 'axios';

import Navbartable from './Navbartable';

export default class CameraOpen extends Component {

  constructor(props) {
    super(props);
    this.takePicture = this.takePicture.bind(this);

    this.state = {
        image: null,
        filter: null,
        showWarning: true,
        showWarning2:true,
        url_list:[]
    }

    this.handleToggleClick = this.handleToggleClick.bind(this);

  }

  onChange = (state) => {
    this.setState(state);
  }

  selectedColor = () => {
    this.setState({
      filter:"color"
    })
}

selectedStyle = () => {
  this.setState({
      filter:"style"
  })
}

confirm = () => {
  axios.post(`http://52.221.240.144:5000/find_similar`, this.state)
  .then(res => {
    const persons = res.data.response;
    this.setState({
        url_list : persons
    })
})
}
handleToggleClick() {
  this.setState(state => ({
    showWarning: !state.showWarning
  }));
}
handleToggleClick2() {
  this.setState(state => ({
    showWarning2: !state.showWarning2
  }));
}

  takePicture() {
    this.camera.capture()
    .then(blob => {
      this.img.src = URL.createObjectURL(blob);
      this.img.onload = () => { 
        URL.revokeObjectURL(this.src); 
        };
        const reader = new FileReader();
        reader.readAsDataURL(blob); 
        reader.onload = () => this.setState({ image: reader.result })
    })
  }

  direction = () => {

  }

  render() {
    console.log(this.state.filter)
    console.log(this.state)

    return (
      <div style={style.container}>
      <Navbartable />
      <h1 style={style.header}>Snap. Suggest. Choose</h1>
        <Camera
          style={style.preview}
          ref={(cam) => {
            this.camera = cam;
          }}
        >
          <div style={style.captureContainer} onClick={() => {this.takePicture(); this.handleToggleClick();}}>
              <div style={style.captureButton} />
          </div>
        </Camera>
        <img
          style={style.captureImage}
          ref={(img) => {
            this.img = img;
          }}
        />
        {this.state.showWarning ? <div></div> : 
        <div style={style.choose}>
          <Button style={style.chooseBtn} onClick={() => {this.selectedColor(); this.handleToggleClick2();}}>Color</Button>
          <Button style={style.chooseBtn} onClick={() => {this.selectedStyle(); this.handleToggleClick2();}}>Style</Button>
        </div>}
        {this.state.showWarning2 ? <div></div> : 
        <div style={style.choose}>
        <Button style={style.confirmBtn} onClick={this.confirm}>Confirm</Button>
        </div>}
      <div>
        <div>
              {this.state.url_list.map(person => 
              <ul>
                  <Card>
                      <CardImg top width="30%" src={person.URL} alt="Card image cap" />
                      <CardBody style={style.card}>
                      <CardTitle>Style</CardTitle>
                      <CardSubtitle style={style.font}>{person.Style}</CardSubtitle>
                      <CardTitle>Color</CardTitle>
                      <CardSubtitle style={style.font}>{person.Colour.toString()}</CardSubtitle>
                      <CardTitle>Gender</CardTitle>
                      <CardSubtitle>{person.Gender}</CardSubtitle>
                      <Button style={style.directionBtn} onClick={this.direction}>Direction</Button>
                      <Button style={style.directionBtn}>Add to cart</Button>
                      </CardBody>
                  </Card>
              </ul>)}
          </div>
        </div>
      </div>
    );
  }
}

const style = {
  font: {
    fontSize:'40px'
  },
  header: {
    textAlign:'center',
    margin:'3%',
    fontFamily: 'Comfortaa',
  },
  choose: {
    display: 'flex',
    justifyContent: 'center',
  },
  chooseBtn:{
    margin: '70px',
    fontSize: '70px',
    fontFamily: 'Comfortaa',
    backgroundColor: '#e89829'
  },
  confirmBtn:{
    margin: '20px',
    backgroundColor: 'green',
    fontSize: '80px',
    fontFamily: 'Comfortaa',
  },
  preview: {
    marginTop: '1%',
    position: 'relative',
    width: '50%',
    display: 'inline-block',

  },
  captureContainer: {
    display: 'flex',
    position: 'absolute',
    justifyContent: 'center',
    zIndex: 1,
    bottom: 0,
    width: '100%'
  },
  captureButton: {
    backgroundColor: '#fff',
    borderRadius: '50%',
    height: 56,
    width: 56,
    color: '#000',
    margin: 20
  },
  captureImage: {
    marginTop: '1%',
    width:'50%',
    display: 'inline-block',
    float: 'right',
  },
  card: {
    textAlign: 'center',
    margin: '20px'
  },
  directionBtn: {
    margin:'20px'
  }
};