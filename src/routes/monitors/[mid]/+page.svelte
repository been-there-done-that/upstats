<script lang="ts">
	import type { PageProps } from './$types';
	import Settings from 'lucide-svelte/icons/settings';
	import ChevronsLeft from 'lucide-svelte/icons/chevrons-left';
	import Pause from 'lucide-svelte/icons/pause';
	import Button from '$lib/components/ui/button/button.svelte';
	import { goto } from '$app/navigation';
	import ExternalLink from 'lucide-svelte/icons/external-link';
	import { toast } from 'svelte-sonner';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { mode } from 'mode-watcher';

	let chart: any;

	var optionsLine = {
		chart: {
			height: 320,
			type: 'line',
			zoom: {
				enabled: false
			},
			dropShadow: {
				enabled: true,
				top: 3,
				left: 2,
				blur: 4,
				opacity: 1
			},
			fontFamily: 'IBM Plex Mono, Helvetica, Arial, sans-serif'
		},
		stroke: {
			curve: 'smooth',
			width: 2
		},
		colors: [$mode == 'light' ? '#000000' : '#ffffff'], // Custom color
		series: [
			{
				name: 'Time Taken (ms)',
				data: [
					{ x: new Date('2024-02-10T10:00:00').getTime(), y: 150 },
					{ x: new Date('2024-02-10T10:05:00').getTime(), y: 180 },
					{ x: new Date('2024-02-10T10:10:00').getTime(), y: 120 },
					{ x: new Date('2024-02-10T10:15:00').getTime(), y: 200 },
					{ x: new Date('2024-02-10T10:20:00').getTime(), y: 170 }
				]
			}
		],
		markers: {
			size: 4,
			strokeWidth: 0,
			hover: {
				size: 6
			}
		},
		grid: {
			show: true,
			xaxis: {
				lines: {
					show: true
				}
			},
			yaxis: {
				lines: {
					show: true
				}
			},
			padding: {
				bottom: 0
			}
		},
		xaxis: {
			type: 'datetime',
			tooltip: {
				enabled: true
			}
		},
		tooltip: {
			enabled: true,
			x: {
				format: 'dd MMM yyyy HH:mm:ss'
			},
			y: {
				formatter: function (value: String) {
					return value + ' ms';
				}
			}
		},
		yaxis: {
			title: {
				text: 'Time (ms)'
			}
		}
	};

	$effect(() => {
		// we need to check chart object exists or not as it is possible it might be empty before onmount happens
		console.log({ chart });
		if ($mode && chart) {
			chart.updateOptions({
				colors: [$mode === 'light' ? '#000000' : '#ffffff']
			});
		}
	});

	onMount(async () => {
		if (browser) {
			const ApexCharts = (await import('apexcharts')).default;
			const chartElement = document.getElementById('chart');
			chart = new ApexCharts(chartElement, optionsLine);
			await chart.render();
		}
	});

	// Cleanup on destroy
	onDestroy(() => {
		if (chart) chart.destroy();
	});

	let { data }: PageProps = $props();

	class MonitorStatus {
		static SUCCESS = 'SUCCESS';
		static ERROR = 'ERROR';
		static PAUSED = 'PAUSED';
	}
</script>

<Button
	variant="ghost"
	onclick={async () => await goto('/')}
	class="text-purple-500 hover:text-purple-600 hover:shadow-md"
>
	<ChevronsLeft strokeWidth={3} />
	<span class="-mx-1 text-base font-semibold italic">Monitors</span>
</Button>

{#snippet Ping(status: string)}
	<div class="relative flex h-12 w-12 items-center justify-center">
		{#if status == MonitorStatus.SUCCESS}
			<div class="h-3 w-3 rounded-full bg-green-500"></div>
			<div class="ping bg-green-500/50"></div>
		{:else if status == MonitorStatus.ERROR}
			<div class="h-3 w-3 rounded-full bg-red-500"></div>
			<div class="ping bg-red-500/50"></div>
		{:else if status == MonitorStatus.PAUSED}
			<div class="h-3 w-3 rounded-full bg-yellow-500"></div>
			<div class="ping bg-yellow-500/50"></div>
		{/if}
	</div>
{/snippet}

<div>
	<div class=" flex">
		<div class="flex items-center justify-center">
			{@render Ping(data.status)}
		</div>
		<div>
			<h1 class="text-2xl font-medium">
				<span>{data.name}</span>
			</h1>
			<div class="text-md flex w-full items-center justify-start gap-3">
				<span
					class="capitalize"
					class:text-yellow-500={data.status == MonitorStatus.PAUSED}
					class:text-green-500={data.status == MonitorStatus.SUCCESS}
					class:text-red-500={data.status == MonitorStatus.ERROR}>{data.status.toLowerCase()}</span
				><span class="text-2xl">&#183;</span> <span>Checked every {data.frequency}</span>
				<span class="text-2xl">&#183;</span>
				<span
					><a
						href={data.url}
						target="_blank"
						class="flex items-center gap-2 text-purple-600 hover:underline"
					>
						<span>{data.url}</span> <ExternalLink size={14} /></a
					></span
				>
			</div>
		</div>
	</div>

	<div class="mx-8 flex flex-col gap-4">
		<div class=" mx-1 my-6 flex flex-col gap-4">
			<div class="my-2 flex flex-row items-end justify-end space-x-3">
				<Button
					variant="outline"
					class="h-8"
					onclick={() => toast.success('We will pause or un Pause')}
					><Pause />
					{#if data.paused}
						Unpause
					{:else}
						Pause
					{/if}
				</Button>
				<Button variant="outline" class="h-8" href={`/monitors/${data.id}/configure`}
					><Settings /> Configure</Button
				>
			</div>
			<div class="mt-5 h-32 rounded-sm border border-gray-200 p-3 shadow-md">
				<table class="w-full">
					<thead>
						<tr class="w-full py-4">
							<th class="w-[30%] border-b border-r py-3">
								<span class="text-base font-medium">Average Response (24 Hour)</span>
							</th>
							<th class="w-[25%] border-b border-r py-3">
								<span class="text-base font-medium">Uptime (24 Hours)</span>
							</th>
							<th class="w-[25%] border-b border-r py-3">
								<span class="text-base font-medium">Uptime (30 days)</span>
							</th>
							<th class="w-[20%] border-b py-3">
								<span class="text-base font-medium">Cert Exp In</span>
							</th>
						</tr>
					</thead>
					<tbody class="">
						<tr>
							<td class="border-r py-3 text-center">
								<span class="text-lg font-semibold">300 ms</span>
							</td>
							<td class="border-r py-3 text-center">
								<span class="text-lg font-semibold">100%</span>
							</td>
							<td class="border-r py-3 text-center">
								<span class="text-lg font-semibold">100%</span>
							</td>
							<td class="py-3 text-center">
								<span class="text-lg font-semibold">64 Days</span>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
	<div
		class="m-8 flex items-center justify-between rounded-lg border border-gray-200/85 p-3 px-4 shadow-md"
	>
		<div id="chart" class="w-full"></div>
	</div>
</div>

<style global>
	:global(.apexcharts-tooltip-marker[shape='circle']::before) {
		content: '>' !important; /* Remove the dot */
	}
</style>
