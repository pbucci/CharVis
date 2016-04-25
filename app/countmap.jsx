export default class CountMap {
  constructor() {
    this.map = new Map()
  }
  add(i,n) {
    if (this.map.has(i)) {
      this.map.set(i,this.map.get(i) + n)
    }
    else {
      this.map.set(i,n)
    }
    return [i,this.map.get(i)]
  }
  get(i) {
    return this.map.get(i)
  }
  keys() {
    return this.map.keys()
  }
  keyvals() {
    return Array.from(this.map.entries());
  }
};
