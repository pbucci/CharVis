import React from 'react';
import d3 from 'd3';

var TextInput = React.createClass({
	getInitialState: function() {
    	return {value: this.props.startvalue};
  	},
  	handleChange: function(event) {
    	this.setState({inputtext:event.target.value})
  	},
    enter: function(e) { 
      if (e.keyCode == 13) {
        this.props.callbackParent(this.props.startvalue,this.state.inputtext);
      }
    },
  	render: function() {
    	return (
      	<input
      		className   = "date_input"
        	type        = "text"
        	placeholder = {this.props.placeholder}
        	onChange    = {this.handleChange} 
          onKeyDown   = {this.enter} />
    );
  }
})

var Navigation = React.createClass({
  getInitialState: function() {
    return {start: this.props.start, end: this.props.end, tags:this.props.tags, speakers:this.props.speakers};
  },
  onChildChanged: function(k,v) {
    var date = new Date(v);
    if (!v) {v=""}
    var obj = {
      start: this.state.start,
      end: this.state.end,
      tags: this.state.tags,
      speakers: this.state.speakers,
    };

    if (k=="end date") {
      obj.end = date; // date string, e.g. 2003/1/2
    } else if (k=="start date") {
      obj.start = date; // date string, e.g. 2003/1/2
    } else if (k=="tags") {

      obj.tags = v.split(' ') // array of tags, e.g. ["ralph","nader"]
    } else if (k=="speakers") {
      obj.speakers = v.split(' ')
    }
      this.props.callbackParent(obj);
      this.setState(obj)
  },

  render: function() {
    return (<div className="navigation">
    			<p><strong>Filter texts by date between</strong></p>
    				
    				<p><strong>{this.props.start.toDateString()}</strong></p>
    				<TextInput startvalue="start date" callbackParent={this.onChildChanged} placeholder="Start date (YYYY/MM/DD)"/>
    				
    				<p><strong>{this.props.end.toDateString()}</strong></p>
    				<TextInput startvalue="end date" callbackParent={this.onChildChanged} placeholder="End date (YYYY/MM/DD)"/>
    			<hr / >
    			<p><strong>Filter by concepts</strong></p>
          <p className="smalltext">Enter full or partial tags for concepts and hit enter. E.g. "Wash" will produce "Washington". Separate tags by a space. Hitting enter on a blank box will produce all concepts, but, just as a warning, that will take some time to process.</p>
    			<TextInput startvalue="tags" callbackParent={this.onChildChanged} placeholder="Enter concepts..." />
          <hr />
          <p><strong>Filter by speakers</strong></p>
          <p className="smalltext">Enter full or partial tags for speakers and hit enter. E.g. "Bill" will produce any speaker with "Bill" in the name.</p>
          <TextInput startvalue="speakers" callbackParent={this.onChildChanged} placeholder="Enter speakers..." />
    		</div>)
  }
});

module.exports = Navigation;