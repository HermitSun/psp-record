function pad(num) {
    return ('0' + num).slice(-2);
}

function currentTime() {
    var now = new Date();
    var year = now.getFullYear(), month = now.getMonth(), day = now.getDay(),
        hours = now.getHours(), minutes = now.getMinutes(), secs = now.getSeconds();
    return year + '-' + pad(month) + '-' + pad(day) + ' ' +
        pad(hours) + ':' + pad(minutes) + ':' + pad(secs);
}

function hhmmss(secs) {
    var minutes = Math.floor(secs / 60);
    secs = secs % 60;
    var hours = Math.floor(minutes / 60);
    minutes = minutes % 60;
    return pad(hours) + ':' + pad(minutes) + ':' + pad(secs);
}


$(document)
    .ready(function () {
        // var isPausing = Boolean(localStorage.getItem('isPausing')) || false;
        var isPausing = false;
        // 计时，先从本地读
        // var pureTime = Number(localStorage.getItem('pureTime')) || 0;
        var pureTime = 0;
        var pureTimer;
        // var pauseTime = Number(localStorage.getItem('pauseTime')) || 0;
        var pauseTime = 0;
        var pauseTimer;
        // 计时功能按钮
        var buttonStartTiming = $('#start-timing');
        var buttonPauseTiming = $('#pause-timing');
        var buttonStopTiming = $('#end-timing');
        // 表格内容
        var itemStartTime = $('#logs-item-start-time');
        var itemPauseTime = $('#logs-item-pause-time');
        var itemEndTime = $('#logs-item-end-time');
        var itemPureTime = $('#logs-item-pure-time');
        var itemBelong = $('#logs-item-belong');
        var itemBacklog = $('#logs-item-backlog');
        // 表格功能按钮
        var buttonResetTiming = $('#add-timing-logs-toolbar button[type="reset"]');
        var buttonSubmitTiming = $('#add-timing-logs-toolbar button[type="submit"]');
        // 计时
        buttonStartTiming.click(function () {
            itemStartTime.text(currentTime());
            // 禁用开始按钮，启用暂停和中止
            buttonStartTiming.attr('disabled', 'true');
            buttonPauseTiming.removeAttr('disabled');
            buttonStopTiming.removeAttr('disabled');
            // 开始计时
            pureTimer = setInterval(function () {
                ++pureTime;
                itemPureTime.text(hhmmss(pureTime));
                // save
                localStorage.setItem('pureTime', pureTime.toString());
            }, 1000);
        });
        buttonPauseTiming.click(function () {
            isPausing = !isPausing;
            // save
            // localStorage.setItem('isPausing', isPausing.toString());
            // 暂停 & 恢复
            buttonPauseTiming.text(isPausing ? '继续计时 ▶' : '暂停计时 ⏸')
            // 暂停时计时，恢复时取消
            if (isPausing) {
                pauseTimer = setInterval(function () {
                    ++pauseTime;
                    itemPauseTime.text(hhmmss(pauseTime));
                    // save
                    // localStorage.setItem('pauseTime', pauseTime.toString());
                }, 1000)
                clearInterval(pureTimer);
            } else {
                clearInterval(pauseTimer);
                pureTimer = setInterval(function () {
                    ++pureTime;
                    itemPureTime.text(hhmmss(pureTime));
                    // save
                    // localStorage.setItem('pureTime', pureTime.toString());
                }, 1000);
            }
        })
        buttonStopTiming.click(function () {
            itemEndTime.text(currentTime());
            resetButtons();
            resetTimers();
        });
        buttonResetTiming.click(function () {
            resetFormItems();
            resetButtons();
            resetTimers();
        })
        buttonSubmitTiming.click(function () {
            var startTime = itemStartTime.text(),
                pauseTime = itemPauseTime.text(),
                endTime = itemEndTime.text(),
                pureTime = itemPureTime.text(),
                belong = itemBelong.val(),
                backlog = itemBacklog.val();
            $.post('/logs', JSON.stringify({
                start_time: startTime,
                pause_time: pauseTime,
                end_time: endTime,
                pure_time: pureTime,
                belong: belong,
                backlog: backlog
            }), function (_, status) {
                if (status === 'success') {
                    alert('保存成功');
                } else {
                    alert('保存失败，请重试');
                }
            })
        })

        // 重置方法
        function resetFormItems() {
            itemStartTime.text('');
            itemPauseTime.text('');
            itemEndTime.text('');
            itemPureTime.text('');
            itemBelong.val('');
            itemBacklog.val('');
        }

        function resetButtons() {
            // 禁用暂停和中止按钮，启用开始按钮
            buttonStartTiming.removeAttr('disabled');
            buttonPauseTiming.attr('disabled', 'true');
            buttonStopTiming.attr('disabled', 'true');
            // 恢复按钮状态
            buttonPauseTiming.text('暂停计时 ⏸');
        }

        function resetTimers() {
            clearInterval(pureTimer);
            clearInterval(pauseTimer);
        }
    });