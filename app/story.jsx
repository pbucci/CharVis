import React from 'react';
import d3 from 'd3';
import $ from 'jquery'
// highlight ------------------------------------------------------------------------
// returns the css class for concept
// tbd whether this is the best way yet
function highlight(concept) {
  // var the_map = {
  //   opinions:"chartreuse",
  //   life:"yellow",
  // }
  return 'yellow'
}

// Words ---------------------------------------------------------------
// Render all the words with concepts highlighted
var Words = React.createClass({
  // stopwords: function(words) {
    
  //   var ret = words.map(function(w){
  //     if (w in stopchars) {
  //       return(<span>{w}</span>)
  //     } else {
  //       return(<span> {w}</span>)
  //     }
  //   })
  // },
  spacemap: function(words) {
    var stopchars = new Set([",",".","!","?","(",")","[","]","\'\'","\'"])
    return words.map(function(w){
      if (stopchars.has(w)) {
        return(<span>{w}</span>)  
      } else {
        return(<span> {w}</span>)
      }
    })
  },
  render: function() {
    var text = this.props.text
    var concepts = this.props.concepts
    var select = this.props.selectedConcept

    var out = []
    var temp = []

    var filtered = concepts.filter(function(c){
      return (c['concept'] == select)
    });
    var s = 0
    var e = text.length
    var signed_text = filtered.forEach(function(f){
      out.push([text.slice(s,f['i']-1),false])
      out.push([text.slice(f['i']-1,f['j']-1),true])
      s = f['j']-1
    });
    out.push([text.slice(s,e),false])
    var ret = out.map(function(o){
      if(o[1]) {
        return(<span className="yellow">{this.spacemap(o[0])}</span>)
      } else {
        return(<span>{this.spacemap(o[0])}</span>)
      }
    }.bind(this))

    return (<span> {ret} </span>)
    return (<div>{ret}</div>)
      }
  });

// Paragraph ------------------------------------------------------------
// Render a single paragraph
var Paragraph = React.createClass({
  render: function() {
    return (
      <div className="paragraph">
        <p><strong>{this.props.speaker}: </strong><Words text={this.props.text} concepts={this.props.concepts} selectedConcept={this.props.selectedConcept}/></p>
      </div>
    );
  }
});

// Paragraphs -----------------------------------------------------------
// Render all paragraphs
var Paragraphs = React.createClass({
  render: function() {
    var select = this.props.selectedConcept
    var paragraphs = this.props.paragraphs.map(function(paragraph) {
      return (
        <Paragraph 
          speaker  = {paragraph['speaker']} 
          text     = {paragraph['text']} 
          concepts = {paragraph['concepts']}
          key      = {paragraph['id']} 
          selectedConcept = {select}/>
      );
    });
    return (
      <div className="paragraphList">
        {paragraphs}
      </div>
    );
  }
});

// Story ---------------------------------------------------------------
// Render a whole story
var Story = React.createClass({
  
   getInitialState: function() {
       return {info: {title:"loading ... ",paragraphs:[ ] } };
    },
    componentDidMount: function() {
      console.log('componentDidMount called')
      $.ajax({
      url: 'texts/' + this.props.text.filename,
      dataType: 'json',
      success: function(data) {
        console.log('success')
        this.setState({info: data});
      }.bind(this),
      error:function(req,status,err){
        console.log(req,status,err)
      },

    });
    },
    mySetState: function(s){
      this.setState(s)
    },
  render: function() {
    return (
      <div className="story">
        <p className="back_button" onClick={this.props.reset}>Back to all texts</p>
        <h3 className="title">{this.props.text.title}</h3>
        <hr />
        <Paragraphs paragraphs={this.state.info.paragraphs} selectedConcept={this.props.selectedConcept}/>
      </div>
    )
  }
});

module.exports = Story;