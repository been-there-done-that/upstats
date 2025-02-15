<script lang="ts">
	import type { PageProps } from './$types';
	import Settings from 'lucide-svelte/icons/settings';
	import ChevronsLeft from 'lucide-svelte/icons/chevrons-left';
	import Pause from 'lucide-svelte/icons/pause';
	import Button from '$lib/components/ui/button/button.svelte';
	import { goto } from '$app/navigation';
	import ExternalLink from 'lucide-svelte/icons/external-link';
	import { toast } from 'svelte-sonner';

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

	<div class="mx-12 flex flex-col gap-4">
		<div class=" mx-1 my-6 flex flex-col gap-4">
			<div class="my-2 flex flex-row items-end justify-end space-x-3">
				<Button variant="outline" class="h-8"
				onclick={() => toast.success("We will pause or un Pause")}
					><Pause />
					{#if data.paused}
						Unpause
					{:else}
						Pause
					{/if}
				</Button>
				<Button variant="outline" class="h-8" href={`/monitors/configure/${data.id}`}><Settings /> Configure</Button>
			</div>

			<div class="grid grid-cols-1 gap-10 md:grid-cols-2 lg:grid-cols-4">
				<div class="col-span-1 h-28 rounded-lg border-gray-200/85 border shadow-md inline-flex flex-col justify-between items-center p-3 px-4">
					<span class="text-base font-medium">Average Response (24 Hour)</span>
					<span class="font-semibold text-xl">300 ms</span>
				</div>
				<div class="col-span-1 h-28 rounded-lg border-gray-200/85 border shadow-md inline-flex flex-col justify-between items-center p-3 px-4">
					<span class="text-base font-medium">Uptime (24 Hours)</span>
					<span class="font-semibold text-xl">100%</span>
				</div>
				<div class="col-span-1 h-28 rounded-lg border-gray-200/85 border shadow-md inline-flex flex-col justify-between items-center p-3 px-4">
					<span class="text-base font-medium">Uptime (30 days)</span>
					<span class="font-semibold text-xl">100%</span>
				</div>
				<div class="col-span-1 h-28 rounded-lg border-gray-200/85 border shadow-md inline-flex flex-col justify-between items-center p-3 px-4">
					<span class="text-base font-medium">Cert Exp In</span>
					<span class="font-semibold text-xl">64 Days</span>
				</div>
			</div>
		</div>
	</div>
</div>
