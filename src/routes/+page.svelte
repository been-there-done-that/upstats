<script lang="ts">
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import { toast } from 'svelte-sonner';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import Ellipsis from 'lucide-svelte/icons/ellipsis';
	import * as Table from '$lib/components/ui/table/index.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';

	// let open = $state(false)

	let selectedRowForDelete: null | any = $state(null);
	let open = $state(false);

	$effect(() => {
		open = !!selectedRowForDelete;
	});

	const invoices = [
		{
			name: 'http://google.com',
			url: 'http://google.com',
			totalAmount: '$250.00',
			frequency: '5 Min'
		}
	];
</script>

<h1 class="text-2xl font-extrabold italic">Monitors</h1>

{open}
{JSON.stringify(selectedRowForDelete)}
<div class="my-8 rounded-lg border text-gray-500 shadow-md hover:text-black dark:text-white w-full">
	<Table.Root>
		<Table.Header>
			<Table.Row>
				<Table.Head class="text-left pl-5 italic text-black">Name</Table.Head>
				<Table.Head class="text-center italic text-black">URL</Table.Head>
				<Table.Head class="text-center italic text-black">Beats</Table.Head>
				<Table.Head class="w-24 text-center italic text-black">Frequency</Table.Head>
				<Table.Head class="w-24 text-center italic text-black">Action</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each invoices as invoice, i (i)}
				<Table.Row class="group">
					<Table.Cell class="text-left pl-5 text-gray-500 group-hover:text-black border dark:text-white"
						>{invoice.name}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black border dark:text-white"
						>{invoice.url}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black border dark:text-white"
						>{invoice.frequency}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black border dark:text-white"
						>{invoice.totalAmount}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-black dark:text-white">
						<DropdownMenu.Root>
							<DropdownMenu.Trigger class={buttonVariants({ variant: 'ghost', size: 'icon' })}
								><Ellipsis /></DropdownMenu.Trigger
							>
							<DropdownMenu.Content>
								<DropdownMenu.Group>
									<DropdownMenu.Item>
										<Button variant="ghost" class="h-5" href="/somewhere">Configure</Button>
									</DropdownMenu.Item>
									<DropdownMenu.Separator />
									<DropdownMenu.Item class="flex items-center justify-center">
										<Button
											variant="ghost"
											class="h-5 w-full"
											onclick={() => (selectedRowForDelete = invoice)}
										>
											Delete
										</Button>
									</DropdownMenu.Item>
								</DropdownMenu.Group>
							</DropdownMenu.Content>
						</DropdownMenu.Root>
					</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>

<!-- This will take care of the logout part -->
<AlertDialog.Root bind:open>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete your account and remove your data
				from our servers.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action
				class={buttonVariants({ variant: 'destructive' })}
				onclick={() => [(open = !open), toast.error('We will Delete This Row from database...')]}
				>Confim</AlertDialog.Action
			>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
