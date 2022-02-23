import React, { Component, PropTypes } from 'react'

export default class FullheightIframe extends Component {

    render() {
        return (
            <iframe
                style={{maxWidth:"100%", width:'100%', height:'calc(100vh - 70px)', overflow:'visible',
                display:'flex',
                flexDirection:'column'}}
                flex={1} overflow="auto"
                ref="iframe"
                src={this.props.url}
                scrolling="no"
                frameBorder="0"
            />
        );
    }
}
