import React from 'react';
import axios from 'axios';
import {Button, Card, CardImg, CardText, CardBody,
    CardTitle, CardSubtitle} from 'reactstrap';

import Navbartable from './Navbartable';

export default class Suggested extends React.Component {

    render() {
        console.log(this.props)
        return (
            <div>
                <Navbartable />
                <div class="row">
                    {this.props.url_list.map(person => 
                    <ul>
                        <Card class="col-sm-2">
                            <CardImg top width="100%" src={person} alt="Card image cap" />
                            <CardBody>
                            <CardTitle>Card title</CardTitle>
                            <CardSubtitle>Card subtitle</CardSubtitle>
                            <CardText>Some quick example text to build on the card title and make up the bulk of the card's content.</CardText>
                            <Button style={style.button}>Button</Button>
                            </CardBody>
                        </Card>
                    </ul>)}
                </div>
            </div>
        )
    }
}

const style ={
    button:{
        color:'green'
    }
}