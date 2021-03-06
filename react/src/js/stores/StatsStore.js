import { EventEmitter } from "events";

import dispatcher from "../dispatcher";

class StatsStore extends EventEmitter {
  constructor() {
    super();
    this.curLeaders = {
      'pts': [],
      'reb': [],
      'ast': [],
      'fgp': [],
      'ftp': [],
      'fg3p': [],
      'stl': [],
      'blk': []
    };
    this.allTimeLeaders = {
      'pts': [],
      'reb': [],
      'ast': [],
      'fgp': [],
      'ftp': [],
      'fg3p': [],
      'stl': [],
      'blk': []
    };
    this.seasonLeaders = {
      'pts': [],
      'reb': [],
      'ast': [],
      'fgp': [],
      'ftp': [],
      'fg3p': [],
      'stl': [],
      'blk': []
    };
    this.curLeadersPics = []
  }

  getCurLeaders() {
    return this.curLeaders;
  }

  getAllTimeLeaders() {
    return this.allTimeLeaders;
  }

  getSeasonLeaders() {
    return this.seasonLeaders;
  }

  getCurLeadersPics() {
    return this.curLeadersPics;
  }

  handleActions(action) {
    switch(action.type) {
      case "RECEIVE_ALL_LEADERS": {
        // console.log("leaders received");
        let curLeaders = {};
        let allTimeLeaders = {}
        const ptsLeaders = action.leaders[0]['resultSet'];
        curLeaders.pts = ptsLeaders[0]['rowSet'];
        console.log(this.curLeaders['pts']);
        allTimeLeaders.pts = ptsLeaders[1]['rowSet'];
        // console.log(ptsLeaders)

        const rebLeaders = action.leaders[1]['resultSet'];
        curLeaders.reb = rebLeaders[0]['rowSet'];
        allTimeLeaders.reb = rebLeaders[1]['rowSet'];
        // console.log(rebLeaders);

        const astLeaders = action.leaders[2]['resultSet'];
        curLeaders.ast = astLeaders[0]['rowSet'];
        allTimeLeaders.ast = astLeaders[1]['rowSet'];
        // console.log(astLeaders);

        const fgpLeaders = action.leaders[3]['resultSet'];
        curLeaders.fgp = fgpLeaders[0]['rowSet'];
        allTimeLeaders.fgp = fgpLeaders[1]['rowSet'];
        // console.log(fgpLeaders);

        const ftpLeaders = action.leaders[4]['resultSet'];
        curLeaders.ftp = ftpLeaders[0]['rowSet'];
        allTimeLeaders.ftp = ftpLeaders[1]['rowSet'];
        // console.log(ftpLeaders);

        const fg3pLeaders = action.leaders[5]['resultSet'];
        curLeaders.fg3p = fg3pLeaders[0]['rowSet'];
        allTimeLeaders.fg3p = fg3pLeaders[1]['rowSet'];
        // console.log(fg3pLeaders);

        const stlLeaders = action.leaders[6]['resultSet'];
        curLeaders.stl = stlLeaders[0]['rowSet'];
        allTimeLeaders.stl = stlLeaders[1]['rowSet'];
        // console.log(stlLeaders);

        const blkLeaders = action.leaders[7]['resultSet'];
        curLeaders.blk = blkLeaders[0]['rowSet'];
        allTimeLeaders.blk = blkLeaders[1]['rowSet'];
        // console.log(blkLeaders);

        this.curLeaders = curLeaders;
        this.allTimeLeaders = allTimeLeaders;
        console.log(curLeaders);
        console.log(allTimeLeaders);

        this.emit("change");
        break;
      }
      case "RECEIVE_SEASON_LEADERS": {
        // console.log(action.leaders);
        let seasonLeaders = {};

        const ptsLeaders = action.leaders[0]['resultSet'];
        seasonLeaders.pts = ptsLeaders[0]['rowSet'];
        // console.log(ptsLeaders)

        const rebLeaders = action.leaders[1]['resultSet'];
        seasonLeaders.reb = rebLeaders[0]['rowSet'];
        // console.log(rebLeaders);

        const astLeaders = action.leaders[2]['resultSet'];
        seasonLeaders.ast = astLeaders[0]['rowSet'];
        // console.log(astLeaders);

        const fgpLeaders = action.leaders[3]['resultSet'];
        seasonLeaders.fgp = fgpLeaders[0]['rowSet'];
        // console.log(fgpLeaders);

        const ftpLeaders = action.leaders[4]['resultSet'];
        seasonLeaders.ftp = ftpLeaders[0]['rowSet'];
        // console.log(ftpLeaders);

        const fg3pLeaders = action.leaders[5]['resultSet'];
        seasonLeaders.fg3p = fg3pLeaders[0]['rowSet'];
        // console.log(fg3pLeaders);

        const stlLeaders = action.leaders[6]['resultSet'];
        seasonLeaders.stl = stlLeaders[0]['rowSet'];
        // console.log(stlLeaders);

        const blkLeaders = action.leaders[7]['resultSet'];
        seasonLeaders.blk = blkLeaders[0]['rowSet'];
        // console.log(blkLeaders);

        this.seasonLeaders = seasonLeaders;
        console.log(seasonLeaders);
        this.emit("changeSeason");
        break;
      }
    }
  }

}

const statsStore = new StatsStore;
dispatcher.register(statsStore.handleActions.bind(statsStore));

export default statsStore;
