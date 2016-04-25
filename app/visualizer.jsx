import React from 'react';

var Bar = React.createClass({
  sentimap: function([k,v]) {
    var base = {
      width:'2px',
      height:'20px',
      float:'left',
    }
    if (v <= 0.4) {
      base.backgroundColor="#888888"
    } else {
      if (k=="pos") {
        if (v <= 0.8) {
          base.backgroundColor="#4B644B"
        }
        else {
          base.backgroundColor="green"
        }
      } else {
        if (v <= 0.8) {
          base.backgroundColor="#644B4B"
        }
        base.backgroundColor="red"
      }
    }
    return base
  },
  render: function() {
    return ( 
      <div style={this.sentimap(this.props.data)} 
           title={  " date: "       + this.props.date + 
                    " sentiment: [" + this.props.data[0] + "," + this.props.data[1] + "]" + 
                    " title: "      + this.props.title }>
      </div>
    )
  }
})

var BarGraph = React.createClass({
  render: function() {
    var concept = this.props.concept
    var count = 0

    var barmap = []
    this.props.data.forEach(function(o){
      o.sentiments.forEach(function(s) {
        barmap.push([s,o.date,o.title])
      });
    })
    
    var count = 0
    var out = barmap.map(function([s,d,t]){
      count++
      return(<Bar key   = {concept + count} 
                  data  = {s} 
                  date  = {d} 
                  title = {t} />)
    });
    return (<div className="graph">{out}</div>)
  }
});

var Visualizer = React.createClass({
  render: function() {
      var callBack = this.props.callBack
      var concepts = this.props.concepts
      var texts = this.props.texts
      if (this.props.onetext) {
        concepts = Object.keys(this.props.the_text.concepts)
        this.props.texts = [this.props.the_text]
      }

      var concept_dictionary = concepts.reduce(function(o, v, i) {
            o[v] = [];
            return o;
      }, {});

          texts.forEach(function(text){
          Object.keys(concept_dictionary).forEach(function(concept){
            if (concept in text.concepts) {
              var obj = { // this becomes 'data' below passed to BarGraph
                date:text.date,
                title:text.title,
                sentiments:text.concepts[concept]
              }
              if (concept in concept_dictionary) {
                concept_dictionary[concept].push(obj)
              }
              
            }
          }.bind(this));
        }.bind(this));

      var out = Object.keys(concept_dictionary).map(function(concept) {
        var data = concept_dictionary[concept];
        return (
          <div key={concept} className="concept">
            <div className="concept_text" onMouseOver={callBack.bind(this,concept)}>
              <strong>{concept}</strong> : {data.length}
            </div>
            <BarGraph concept={concept} data={data} />
          </div>
        )
      })
    return (
      <div className="sentiments">
        {out}
      </div>
    )
  },
});


module.exports = Visualizer;