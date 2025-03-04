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
	import { FREQUENCY } from '$lib/utils';
	import { PUBLIC_BASE_URL } from '$env/static/public';
	import { page } from '$app/state';

	let chart: any;

	let data: {
		logs: Array<any>;
		name: string;
		url: string;
		frequency: number;
	} = $state({
		logs: [],
		name: '',
		url: '',
		frequency: 0
	});

	var options = {
		chart: {
			type: 'area',
			height: 320
		},
		colors: ['#000'],
		markers: {
			size: 2,
			strokeWidth: 0,
			hover: {
				size: 6,
				sizeOffset: 3
			}
		},
		stroke: {
			width: 2,
			curve: 'smooth'
		},
		fill: {
			type: 'gradient'
		},
		dataLabels: {
			enabled: false
		},
		series: [],
		noData: {
			text: 'Loading...'
		}
	};

	$effect(() => {
		// we need to check chart object exists or not as it is possible it might be empty before onmount happens
		if ($mode && chart) {
			chart.updateOptions({
				colors: [$mode === 'light' ? '#000000' : '#ffffff']
			});
		}
	});

	const fetchEventLogs = async () => {
		let url = `${PUBLIC_BASE_URL}/api/v1/event/${page.params.mid}/logs`;
		const r = await fetch(url);
		const events = await r.json();
		data = events;
	};

	onMount(async () => {
		await fetchEventLogs();
		if (browser) {
			const ApexCharts = (await import('apexcharts')).default;
			const chartElement = document.getElementById('chart');
			chart = new ApexCharts(chartElement, options);
			await chart.render();
			console.log(data.logs);

			chart.updateSeries([
				{
					name: 'Something',
					data: data.logs.map((r) => {
						return { x: new Date(r.x).toLocaleTimeString(), y: r.y };
					})
				}
			]);
		}
	});

	// Cleanup on destroy
	onDestroy(() => {
		if (chart) chart.destroy();
	});

	// let { data }: PageProps = $props();

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
			{@render Ping('SUCCESS')}
		</div>
		<div>
			<h1 class="text-2xl font-medium">
				<span>{data.name}</span>
			</h1>
			<div class="text-md mt-6 flex w-full flex-col items-center justify-start gap-3">
				<span class="ml-4"
					>Checked: every {Object.keys(FREQUENCY).find(
						(key) => FREQUENCY[key] === data.frequency
					)}</span
				>
				<span class="ml-9 w-full"
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

	<div class="mx-2 flex flex-col gap-4 lg:mx-8">
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
			<div class="mt-5 h-fit rounded-sm border border-gray-200 p-3 shadow-md">
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
		class="m-2 flex items-center justify-between rounded-lg border border-gray-200/85 p-3 px-4 shadow-md lg:m-8"
	>
		<div id="chart" class="w-full"></div>
	</div>
</div>

<style global>
	:global(.apexcharts-tooltip-marker[shape='circle']::before) {
		content: '>' !important; /* Remove the dot */
	}
</style>
