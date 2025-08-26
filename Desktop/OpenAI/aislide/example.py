<html lang="zh-TW"><head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>糖尿病與慢性腎臟病患者 GMI 與 HbA1c 不一致性分析</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Noto Sans TC', sans-serif;
            overflow: hidden;
        }
        .slide-container {
            width: 1280px;
            min-height: 720px;
            background-color: #ffffff;
        }
        .chart-container {
            width: 100%;
            height: 350px;
        }
        .highlight-text {
            color: #b91c1c;
            font-weight: bold;
        }
    </style>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script></head>
<body>
    <div class="slide-container p-10">
        <div class="flex justify-between items-start mb-6">
            <h1 class="text-3xl font-bold text-gray-800">糖尿病與慢性腎臟病患者 GMI 與 HbA1c 不一致性分析</h1>
            <div class="text-sm text-gray-500">
                Oriot P et al. J Diabetes Sci Technol. 2023
            </div>
        </div>

        <div class="grid grid-cols-5 gap-6">
            <div class="col-span-3">
                <h2 class="text-xl font-semibold mb-4">HbA1c 與 GMI 相對差異比較</h2>
                <div class="chart-container mb-4">
                    <canvas id="discordanceChart" style="display: block; box-sizing: border-box; height: 350px; width: 710px;" width="1420" height="700"></canvas>
                </div>
                <div class="flex justify-center items-center space-x-8 text-sm">
                    <div class="flex items-center">
                        <div class="w-4 h-4 bg-blue-500 mr-2"></div>
                        <span>CKD 患者 (慢性腎臟病)</span>
                    </div>
                    <div class="flex items-center">
                        <div class="w-4 h-4 bg-red-500 mr-2"></div>
                        <span>非 CKD 患者</span>
                    </div>
                </div>
            </div>

            <div class="col-span-2">
                <div class="bg-red-50 p-5 rounded-lg mb-6">
                    <h2 class="text-xl font-semibold mb-3">關鍵發現</h2>
                    <ul class="space-y-3">
                        <li class="text-lg"><span class="highlight-text">68.2%</span> 的慢性腎臟病患者 HbA1c 與 GMI 絕對差值 <span class="highlight-text">&gt;0.5%</span></li>
                        <li>CKD 患者的差異顯著高於非 CKD 患者</li>
                        <li>差異在相對差值 &gt;0.3% 時更為明顯</li>
                    </ul>
                </div>

                <div class="bg-gray-50 p-5 rounded-lg">
                    <h2 class="text-xl font-semibold mb-3">臨床意義</h2>
                    <ul class="list-disc pl-5 space-y-2 text-gray-700">
                        <li>慢性腎臟病可能導致 HbA1c 與 GMI 測量值產生更大差異</li>
                        <li>CKD 患者的血糖控制評估應考慮此不一致性</li>
                        <li>臨床醫師在解讀 CKD 患者的血糖指標時需特別謹慎</li>
                        <li>單一指標可能無法準確反映 CKD 患者的真實血糖狀況</li>
                        <li>建議使用多重指標進行綜合評估</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="mt-6">
            <div class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-lg font-semibold mb-2">為什麼 CKD 患者存在更大差異？</h3>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <ul class="list-disc pl-5 space-y-1 text-gray-700">
                            <li>慢性腎臟病影響紅血球壽命，可能導致 HbA1c 偏低</li>
                            <li>尿毒症狀態可能影響糖化過程</li>
                            <li>貧血和紅血球生成素治療影響 HbA1c 測量</li>
                        </ul>
                    </div>
                    <div>
                        <ul class="list-disc pl-5 space-y-1 text-gray-700">
                            <li>GMI 基於連續血糖監測（CGM），不受紅血球代謝影響</li>
                            <li>腎功能損害可能改變糖代謝日間變化模式</li>
                            <li>CKD 患者可能有更大的血糖波動</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="mt-6 border-t pt-3 text-sm text-gray-600 flex justify-between">
            
            <div>相對差異在 90 天使用間歇性掃描式連續血糖監測(isCGM)後測量</div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const ctx = document.getElementById('discordanceChart').getContext('2d');
            
            // 數據基於圖表中的大約值
            const labels = ['≤0.1', '>0.1', '>0.2', '>0.3', '>0.4', '>0.5', '>0.6', '>0.7', '>0.8', '>0.9', '>1.0'];
            const ckdData = [5, 95, 85, 80, 73, 68, 55, 50, 47, 40, 35];
            const nonCkdData = [12, 88, 76, 66, 53, 42, 37, 30, 23, 19, 15];
            
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'CKD患者',
                            data: ckdData,
                            backgroundColor: '#3b82f6',
                            borderColor: '#2563eb',
                            borderWidth: 1
                        },
                        {
                            label: '非CKD患者',
                            data: nonCkdData,
                            backgroundColor: '#ef4444',
                            borderColor: '#dc2626',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: '個體百分比 (%)'
                            },
                            max: 100
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'HbA1c-GMI (%) 相對差異'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                boxWidth: 12,
                                padding: 15
                            }
                        },
                        tooltip: {
                            callbacks: {
                                title: function(tooltipItems) {
                                    return `相對差異 ${tooltipItems[0].label}`;
                                }
                            }
                        }
                    }
                }
            });
            
            // 添加垂直線表示 >0.5% 的臨界點
            const verticalLine = {
                id: 'verticalLine',
                afterDraw: chart => {
                    const ctx = chart.ctx;
                    const xAxis = chart.scales.x;
                    const yAxis = chart.scales.y;
                    const index = 5; // >0.5 的位置
                    
                    ctx.save();
                    ctx.beginPath();
                    ctx.moveTo(xAxis.getPixelForValue(labels[index]), yAxis.top);
                    ctx.lineTo(xAxis.getPixelForValue(labels[index]), yAxis.bottom);
                    ctx.lineWidth = 2;
                    ctx.strokeStyle = 'rgba(220, 38, 38, 0.5)';
                    ctx.stroke();
                    
                    // 添加標籤 - 修改: 增加距離頂部的空間，避免文字被切掉
                    ctx.textAlign = 'center';
                    ctx.fillStyle = '#dc2626';
                    
                    // 繪製一個淺色背景以增強可讀性
                    const text = '臨界點 >0.5%';
                    const textWidth = ctx.measureText(text).width;
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
                    ctx.fillRect(
                        xAxis.getPixelForValue(labels[index]) - textWidth/2 - 5, 
                        yAxis.top - 35, 
                        textWidth + 10, 
                        25
                    );
                    
                    // 繪製文字，移得更高以避免被切到
                    ctx.fillStyle = '#dc2626';
                    ctx.fillText(text, xAxis.getPixelForValue(labels[index]), yAxis.top - 20);
                    
                    ctx.restore();
                }
            };
            
            Chart.register(verticalLine);
        });
    </script>

<script src="https://www.genspark.ai/slide-inner.js?_v=1"></script>
    <script id="html_badge_script1">
        window.__genspark_remove_badge_link = "https://www.genspark.ai/api/html_badge/" +
            "remove_badge?token=To%2FBnjzloZ3UfQdcSaYfDhMzdIn4Op2Cd495f%2FEr42P4niXhRoGvbNYRU87RAxBch7IdRMgu6U4pS%2Bw7VSQ4AURgII7bmCoUqfeac1Wu3osSPE0WeA5i3JHgCK%2FCMSCOGaraMDQ6oSl9l7zV2eHktGYajoHILQoM6AKkdLjC3P9XUb1V0SdCP%2BypGeqMSp7Ft%2B%2FyDfaHd467HEEhfm%2B69QIJNa4TgDvBrP0GaGvNMHdWuGxEYbez7evojfgNeLGQKKzcdtgLzZ2yJCENMPC3DDB3P9i3QIj26cD7tDHeFE1A2nZW3KPQX4qc20%2BXmRZtgoDT2m4v2TvsWElaj7CPgw%2B%2BDX1DHC88WEqbLkzosJ2Yzk5pVF2VD3fw3MjocUt63fbCM791Nn3GXFgh52DGfnzN2gOI4go0keTlExC%2Fsob%2FXPAFFxdaaCBAglwNHARnvKOKMZjwc3%2Fzy5wdFPDSaYwLfPCrpTp5giQE7O5mQM3Ki9dAaqLKSPGaZSKpDSNNG%2F7KPmTcAhkuzrjoJwE0f26pXyVJEmXN1quc6BKRE9%2Bro79IGc278o3RY2o8qeNNwMEwgM2IX2k3Fsnaeah3fNoazu6jEOJWnMmlAm39vPRElLRlB2ZRbdxpIatOQO87crECyBhmKxbAoXZgiEdqURzDE%2F58%2Fa4Bqd%2Bv%2FvGLCdg%3D";
        window.__genspark_locale = "zh-TW";
        window.__genspark_token = "To/BnjzloZ3UfQdcSaYfDhMzdIn4Op2Cd495f/Er42P4niXhRoGvbNYRU87RAxBch7IdRMgu6U4pS+w7VSQ4AURgII7bmCoUqfeac1Wu3osSPE0WeA5i3JHgCK/CMSCOGaraMDQ6oSl9l7zV2eHktGYajoHILQoM6AKkdLjC3P9XUb1V0SdCP+ypGeqMSp7Ft+/yDfaHd467HEEhfm+69QIJNa4TgDvBrP0GaGvNMHdWuGxEYbez7evojfgNeLGQKKzcdtgLzZ2yJCENMPC3DDB3P9i3QIj26cD7tDHeFE1A2nZW3KPQX4qc20+XmRZtgoDT2m4v2TvsWElaj7CPgw++DX1DHC88WEqbLkzosJ2Yzk5pVF2VD3fw3MjocUt63fbCM791Nn3GXFgh52DGfnzN2gOI4go0keTlExC/sob/XPAFFxdaaCBAglwNHARnvKOKMZjwc3/zy5wdFPDSaYwLfPCrpTp5giQE7O5mQM3Ki9dAaqLKSPGaZSKpDSNNG/7KPmTcAhkuzrjoJwE0f26pXyVJEmXN1quc6BKRE9+ro79IGc278o3RY2o8qeNNwMEwgM2IX2k3Fsnaeah3fNoazu6jEOJWnMmlAm39vPRElLRlB2ZRbdxpIatOQO87crECyBhmKxbAoXZgiEdqURzDE/58/a4Bqd+v/vGLCdg=";
    </script>
    </body></html>
