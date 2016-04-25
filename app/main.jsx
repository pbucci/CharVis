// main.js

import React from 'react';

var TAFFY = require('./taffy.js');
var texts = require("json!./summary_reduce.json");

var Visualizer = require('./visualizer.jsx');
var Navigation = require('./navigation.jsx');
var Story      = require('./story.jsx');

// Original cannonical set of all concepts
var concepts = new Set()
texts.forEach(function(t){
  Object.keys(t.concepts).forEach(function(c){
    concepts.add(c)
  })
})

var speakers = new Set()
texts.forEach(function(t){
  t.speakers.forEach(function(sp){
    speakers.add(sp)
  })
})

var OneText = React.createClass({
  render: function() {
    return(<li className="text_list_item"
               onClick={this.props.updateTitle.bind(this,this.props.text.title,this.props.text)}>
               <span><strong>{this.props.text.date} </strong>{this.props.text.title}</span>
           </li>)
  }
});

var Texts = React.createClass({
  render: function() {

    var all_texts = this.props.texts.map(function(t){
        return (<OneText text={t} updateTitle={this.props.updateTitle}/>)
    }.bind(this));
    return(<ul className="text_list">{all_texts}</ul>)
  }
});

var Chooser = React.createClass({
  render: function() {
    var start    = this.props.start
    var end      = this.props.end
    var concepts = new Set(this.props.concepts)
    var title    = this.props.title
    var texts    = this.props.texts

    if (this.props.onetext) {
        this.props.onetextCallback.bind(this,true,texts);
         return (<Story text            = {this.props.the_text} 
                        selectedConcept = {this.props.selectedConcept} 
                        reset           = {this.props.updateTitle.bind(this,"null",null)}/>)
    } else {
        this.props.onetextCallback.bind(this,false,null);  
        return (<Texts texts={texts} updateTitle={this.props.updateTitle} />)
    }
  }
})

var cache = {}

// Main function
var Main = React.createClass({
  getInitialState: function() {
    var ret = {
      start: new Date("2003/01/01"),
      end: new Date(),
      concepts:[],
      title:"null",
      selectedConcepts:[],
      selectedConcept:"",
      onetext:false,
      speakers:[],
    }
    return ret
  }, 
  dataSelect: function(data,start,end,concept_array,speaker_array) {
      var hash = start.toDateString() + end.toDateString() + concept_array.toString() + speaker_array.toString()

      if (hash in cache) {
        return cache[hash]
      }

      var filtered = data.filter(function(d){
            // Filter by date
            var c_date = new Date(d.date)
            if (c_date > end || c_date < start) {
              return false;
            }
            // Filter by concept
            if (concept_array.length > 0) {
              var cfilter = concept_array.some(function(cpt){
                        return (cpt in d.concepts)
                    });
              return cfilter;
            }
            if (speaker_array.length > 0) {
              var sfilter = speaker_array.some(function(spkr){
                return (spkr in d.speakers)
              });
            }
      });

      cache[hash] = filtered
      return filtered;
  },
  setNav: function(o) {
    var obj = o;
    var changed = false;
    if (o.tags != this.state.tags) {
      changed = true;
      obj.concepts = []
      Array.from(concepts).forEach(function(concept){
        o.tags.some(function(tag) {
          if (concept.includes(tag)) {
            obj.concepts.push(concept)
          }
        })
      })
    }
    if (o.start != this.state.start) {
      changed = true;
      obj.start = o.start;
    }
    if (o.end != this.state.end) {
      changed = true;
      obj.end = o.end;
    }

    if (o.speakers != this.state.speakers) {
      changed =  true;
      obj.speakers = []
      Array.from(speakers).forEach(function(speaker){
        o.speakers.some(function(tag) {
          if (speaker.includes(tag)) {
            obj.speakers.push(speaker)
          }
        })
      })

    }

    if (changed) {
      this.setState(obj)
    }
  },
  conceptCallBack: function(data){
    this.setState({selectedConcept:data})
  },
  updateTitle: function(x,the_text) {
    if (x != "null") {
      this.setState({title:x,onetext:true,the_text:the_text});
    } else {
      this.setState({title:x,onetext:false})
    }
  },
  onetext: function(t,the_text) {
    this.setState({onetext:t,the_text:the_text})
  },
  render: function() {
  	var data_reduce = this.dataSelect(texts,
                                      this.state.start,
                                      this.state.end,
                                      this.state.concepts,
                                      this.state.speakers
                                     )
    
    return (  
      <div>
        <div className="header"><h1 className="header_title">CharVis</h1></div>
        <div className="the_content">
          <Navigation start          = {this.state.start}
                      end            = {this.state.end}
                      concepts       = {this.state.concepts}
                      speakers       = {this.state.speakers}
                      callbackParent = {this.setNav} />

          <div className="story">
            <Chooser start           = {this.state.start}
                     end             = {this.state.end}
                     concepts        = {this.state.concepts}
                     selectedConcept = {this.state.selectedConcept}
                     the_text        = {this.state.the_text}
                     title           = {this.state.title}

                     texts           = {data_reduce}
                     updateTitle     = {this.updateTitle}
                     onetext         = {this.state.onetext}
                     onetextCallback = {this.onetext}
          />
          </div>
           <Visualizer texts         = {data_reduce}
                       concepts      = {this.state.concepts}
                       onetext       = {this.state.onetext}
                       the_text       = {this.state.the_text}
                       callBack      = {this.conceptCallBack}
        />
        </div>
      </div>
    )
  }
})

module.exports = Main;