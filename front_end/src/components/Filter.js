import React from 'react';
import {Button} from 'reactstrap';
import axios from 'axios';

// import CameraOpen from 'Cameraopen';

export default class Filter extends React.Component{
    constructor(props) {
        super(props);
        this.selectedColor = this.selectedColor.bind(this);
        this.selectedStyle = this.selectedStyle.bind(this)
        
        this.state = {
            image: '',
            filter: '',
        }
    }

    selectedColor(){
        this.setState({
            filter:'color'
        })
        axios.post(`http://52.221.240.144:5000/find_similar`, this.state)
            .then(res => {
            console.log(res);
            console.log(res.data);
        })
    }

    selectedStyle(){
        this.setState({
            filter:'style'
        })
        axios.post(`http://52.221.240.144:5000/find_similar`, this.state)
            .then(res => {
            console.log(res);
            console.log(res.data);
        })
    }

    render(){
        console.log(this.state)
        return(
            <div>
                <Button onClick={this.selectedColor}>Color</Button>
                <Button onClick={this.selectedStyle}>Style</Button>
            </div>
        )
    }
}