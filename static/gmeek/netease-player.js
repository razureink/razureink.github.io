(function () {
  var PLAYLIST_ID = '18204074828';
  var API = 'https://api.injahow.cn/meting/?server=netease&type=playlist&id=' + PLAYLIST_ID;
  document.addEventListener('DOMContentLoaded', function () {
    if (!window.APlayer) return;
    fetch(API)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (list) {
        if (!list || !list.length) return;
        var audio = list.map(function (s) {
          return {
            name: s.name || '未知歌曲',
            artist: s.artist || '未知歌手',
            url: s.url,
            cover: s.pic || s.cover || '',
            lrc: s.lrc || ''
          };
        });
        var container = document.createElement('div');
        document.body.appendChild(container);
        window.neteasePlayer = new APlayer({
          container: container,
          fixed: true,
          autoplay: false,
          listmaxheight: '340px',
          preload: 'metadata',
          audio: audio
        });
      })
      .catch(function (e) {
        console.log('网易云歌单加载失败:', e);
      });
  });
})();
