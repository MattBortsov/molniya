/* ============================================================
   Молния Тех — единственный источник правды для юр. реквизитов.
   Меняешь данные здесь — обновляется футер и страница privacy.html.
   (Organization JSON-LD в index.html дублирует эти значения вручную,
   т.к. поисковые боты не всегда исполняют JS для structured data.)
   ============================================================ */
window.MT_LEGAL = {
  entityName: 'ИП Нестеренко Илья Александрович',
  founderName: 'Илья Нестеренко',
  inn: '272198132745',
  ogrnip: '323784700337272',
  city: 'Санкт-Петербург',
};

document.addEventListener('DOMContentLoaded', function () {
  var L = window.MT_LEGAL;

  document.querySelectorAll('[data-mt-legal="entity-short"]').forEach(function (el) {
    el.textContent = L.entityName + ' · ИНН ' + L.inn + ' · ' + L.city;
  });

  document.querySelectorAll('[data-mt-legal="entity-full"]').forEach(function (el) {
    el.textContent = L.entityName + ', ИНН ' + L.inn + ', ОГРНИП ' + L.ogrnip + ', ' + L.city;
  });
});
