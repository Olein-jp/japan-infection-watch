const libraryUrl = 'https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js';
const viewUrl = new URL('https://public.tableau.com/views/__16470709141460/1');
viewUrl.searchParams.set('疾患・症状の区分', '3');

const button = document.querySelector('#start');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
const container = document.querySelector('#view');

button.addEventListener('click', async () => {
  button.disabled = true;
  status.textContent = '公式ライブラリを読み込み中';

  let viz;
  let finished = false;

  function stop(message) {
    if (finished) return;
    finished = true;
    clearTimeout(timeout);
    status.textContent = message;
    viz?.remove();
  }

  const timeout = setTimeout(() => {
    stop(`60秒で終了しました（${status.textContent}）。`);
  }, 60000);

  try {
    const { TableauViz, TableauEventType } = await import(libraryUrl);
    if (finished) return;

    viz = new TableauViz();
    viz.src = viewUrl.href;
    viz.width = '100%';
    viz.height = '720px';
    viz.toolbar = 'hidden';
    status.textContent = 'FirstInteractive を待機中';

    viz.addEventListener(TableauEventType.VizLoadError, (event) => {
      const { errorCode, message } = event.detail ?? {};
      stop(`ビューの読み込みに失敗しました。 ${[errorCode, message].filter(Boolean).join(' ')}`);
    }, { once: true });

    viz.addEventListener(TableauEventType.FirstInteractive, async () => {
      if (finished) return;
      status.textContent = 'FirstInteractive を受信。シート名とフィルター名を確認中';

      try {
        const { activeSheet, publishedSheetsInfo } = viz.workbook;
        const worksheets = activeSheet.worksheets ?? [activeSheet];
        const report = {
          activeSheet: activeSheet.name,
          sheetType: activeSheet.sheetType,
          publishedSheets: publishedSheetsInfo.map((sheet) => sheet.name),
          worksheets: worksheets.map((sheet) => sheet.name),
        };
        result.textContent = JSON.stringify(report, null, 2);

        // フィルターの値や集計行は記録しない。
        const filters = await activeSheet.getFiltersAsync();
        if (finished) return;
        report.filterNames = [...new Set(filters.map((filter) => filter.fieldName))];
        result.textContent = JSON.stringify(report, null, 2);
        finished = true;
        clearTimeout(timeout);
        status.textContent = 'FirstInteractive を受信。名前の確認が完了しました。';
      } catch (error) {
        stop(`FirstInteractive を受信。名前の確認に失敗しました。 ${error.message}`);
      }
    }, { once: true });

    container.append(viz);
  } catch (error) {
    stop(`初期化に失敗しました。 ${error.message}`);
  }
}, { once: true });
