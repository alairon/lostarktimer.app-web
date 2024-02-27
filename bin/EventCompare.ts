const localData = require('../data/data.json');
const webEvents = require('../data/events.json');
const core = require('@actions/core');

export class EventCompare {
  public static compareData(): Array<String|Number>{
    const Ids: Set<String> = new Set();
    const tempIds: Array<String> = [];
    
    Object.keys(localData).forEach((month) => {
      Object.keys(localData[month]).forEach((day) => {
        Object.keys(localData[month][day]).forEach((ilvl) => {
          Object.keys(localData[month][day][ilvl]).forEach((eventId) => {
            Object.keys((localData[month][day][ilvl][eventId])).forEach((key) => {
              tempIds.includes(key) ? null : tempIds.push(key);
            })
          })
        })
      })
    });
    
    const webEventIds: Array<String> = Object.keys(webEvents);
    const diff = tempIds.filter(x => !webEventIds.includes(x));
    
    if (diff.length > 0){
      core.debug(`${JSON.stringify(diff)} isn't in the event data JSON!`);
      core.setFailed(`Found missing values ${JSON.stringify(diff)} that were not found in the event data JSON.`);
    }
    
    return(diff);
  }
}

module.exports = EventCompare;