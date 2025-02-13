let isLoggedIn = false; //로그인 여부 변수

//캘린더
function convertToISO(dateStr) {
  let date = new Date(dateStr);
  return date.toISOString();
}

document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    headerToolbar: {
      left: "prev today",
      center: "title",
      right: "next",
    },
    events: function (info, successCallback, failureCallback) {
      // fullcalendar 형식으로 변환
      $.ajax({
        type: "GET",
        url: "/calendar",
        success: function (response) {
          let events = [
            ...response.academic_calendar,
            ...response.user_calendar,
          ].map(function (item) {
            return {
              title: item.title,
              start: convertToISO(item.start),
              end: convertToISO(item.end),
            };
          });
          successCallback(events);
        },
        error: function () {
          failureCallback();
        },
      });
    },
    datesSet: function () {
      updateEventColors(); // 월 변경될 때 실행
    },

    eventDidMount: function (info) {
      //tooltip
      tippy(info.el, {
        content: `${
          info.event.end &&
          info.event.start.toLocaleDateString() !==
            info.event.end.toLocaleDateString()
            ? `${info.event.start.toLocaleDateString()} - ${info.event.end.toLocaleDateString()}`
            : info.event.title // 단기 일정은 이벤트 이름 출력
        }`,
        placement: "bottom",
        offset: [0, 0],
        interactive: true,
      });
    },
  });
  calendar.render();

  document.querySelectorAll(".fc-button-primary").forEach((button) => {
    button.addEventListener("click", updateEventColors);
  });
  updateEventColors(); // 초기실행

  // 일정 추가
  function postUser() {
    $.ajax({
      url: "/check-session",
      type: "GET",
      contentType: "application/json",
      data: JSON.stringify({}),
      success: function (response) {
        if (response.success) {
          var title = $("#title").val();
          var start = $("#start").val();
          var end = $("#end").val();

          $.ajax({
            type: "POST",
            url: "/calendar",
            data: {
              title_give: title,
              start_give: start,
              end_give: end,
            },
            success: function (response) {
              alert(response.message);
              calendar.refetchEvents(); // 일정추가 후 달력 새로고침
              updateEventColors()
            },
            error: function () {
              alert("일정을 추가하는데 실패했습니다");
            },
          });
        } else {
          alert("일정을 추가하는데 실패했습니다.");
          return false;
        }
      },
      error: function () {
        alert("일정 추가 도중 오류가 발생했습니다.");
      },
    });
  }

  // 일정 추가 버튼 이벤트
  $("#addEventButton").on("click", function () {
    postUser();
  });
});

const colors = ["#cdf3de", "#d3d6ee", "#faead4", "#fbd6df"]; //색상 배열

// 색상을 순차적으로 변경
function updateEventColors() {
  $.ajax({
    type: "GET",
    url: "/calendar",
    data: {},
    success: function (response) {
      let calendar_list = response["academic_calendar"];
      let events_length = calendar_list.length;

      // 일정 개수만큼 루프 실행
      $(".fc-event-title-container").each(function (index) {
        let colorIndex = index % colors.length; // 순환 색상 적용
        $(this).css("background-color", colors[colorIndex]);
      });
    },
    error: function () {
      console.error("일정 데이터를 불러오는 데 실패했습니다.");
    },
  });
}

// 캘린더 로딩 완료 후 색상 변경 실행
document.addEventListener("DOMContentLoaded", function () {
  updateEventColors();
});
