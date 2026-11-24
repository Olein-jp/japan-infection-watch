const libraryUrl = 'https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js';
const sampleUrl = 'https://public.tableau.com/views/Superstore_embedded_800x800/Overview';
const pageSize = 2;
const exportRowLimit = 12;

const startButton = document.querySelector('#start');
const sheetSelect = document.querySelector('#sheet');
const readButton = document.querySelector('#read');
const exportButton = document.querySelector('#export');
const status = document.querySelector('#status');
const result = document.querySelector('#result');
const container = document.querySelector('#view');

startButton.addEventListener('click', async () => {
  startButton.disabled = true;
  status.textContent = '公式ライブラリを読み込み中';
  let viz;
  let stopped = false;

  function stop(message) {
    stopped = true;
    clearTimeout(loadTimeout);
    status.textContent = message;
    viz?.remove();
    sheetSelect.disabled = true;
    readButton.disabled = true;
    exportButton.disabled = true;
  }

  const loadTimeout = setTimeout(() => stop('60秒で表示確認を終了しました。'), 60000);

  try {
    const { TableauViz, TableauEventType, CrosstabFileFormat } = await import(libraryUrl);
    if (stopped) return;

    viz = new TableauViz();
    viz.src = sampleUrl;
    viz.width = '100%';
    viz.height = '820px';
    viz.toolbar = 'bottom';
    status.textContent = 'FirstInteractive を待機中';

    viz.addEventListener(TableauEventType.VizLoadError, (event) => {
      const { errorCode, message } = event.detail ?? {};
      stop(`読み込みエラー ${[errorCode, message].filter(Boolean).join(' ')}`);
    }, { once: true });

    viz.addEventListener(TableauEventType.FirstInteractive, () => {
      if (stopped) return;
      clearTimeout(loadTimeout);
      const dashboard = viz.workbook.activeSheet;
      const worksheets = dashboard.worksheets ?? [dashboard];
      sheetSelect.replaceChildren(...worksheets.map((sheet) => new Option(sheet.name)));
      sheetSelect.disabled = false;
      readButton.disabled = false;
      status.textContent = 'FirstInteractive を受信。照合するシートを選択してください。';

      readButton.addEventListener('click', async () => {
        readButton.disabled = true;
        sheetSelect.disabled = true;
        status.textContent = '集計の先頭1ページを取得中';
        const worksheet = worksheets[sheetSelect.selectedIndex];

        try {
          const reader = await worksheet.getSummaryDataReaderAsync(pageSize);
          let totalRowCount;
          try {
            totalRowCount = reader.totalRowCount;
            const page = reader.pageCount > 0 && totalRowCount > 0 ? await reader.getPageAsync(0) : null;
            if (page && page.data.length > pageSize) {
              throw new Error('取得行数が指定した上限を超えました。');
            }
            result.textContent = JSON.stringify({
              dashboard: dashboard.name,
              worksheet: worksheet.name,
              pageCount: reader.pageCount,
              totalRowCount,
              retrievedRows: page?.data.length ?? 0,
              columns: page?.columns.map(({ fieldName, dataType }) => ({ fieldName, dataType })) ?? [],
              sample: page?.data.map((row) => row.map(({ value, formattedValue }) => ({
                value, formattedValue,
              }))) ?? [],
            }, null, 2);
          } finally {
            await reader.releaseAsync();
          }

          if (!Number.isInteger(totalRowCount) || totalRowCount < 1 || totalRowCount > exportRowLimit) {
            status.textContent = `集計を確認しました。CSV の対象は1〜${exportRowLimit}行に限ります。`;
            return;
          }
          status.textContent = '集計を確認しました。同じ表示条件で CSV を出力できます。';
          exportButton.disabled = false;

          exportButton.addEventListener('click', async () => {
            exportButton.disabled = true;
            status.textContent = '公式 CSV を出力中';
            try {
              await viz.exportCrosstabAsync(worksheet.name, CrosstabFileFormat.CSV);
              status.textContent = '公式 CSV の出力 API が完了しました。ブラウザのダウンロードを確認してください。';
            } catch (error) {
              stop(`CSV の出力エラー ${error.message}`);
            }
          }, { once: true });
        } catch (error) {
          stop(`集計の取得エラー ${error.message}`);
        }
      }, { once: true });
    }, { once: true });

    container.append(viz);
  } catch (error) {
    stop(`初期化エラー ${error.message}`);
  }
}, { once: true });
