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
			invoice: 'INV001',
			paymentStatus: 'Paid',
			totalAmount: '$250.00',
			paymentMethod: 'Credit Card'
		},
		{
			invoice: 'INV002',
			paymentStatus: 'Pending',
			totalAmount: '$150.00',
			paymentMethod: 'PayPal'
		},
		{
			invoice: 'INV003',
			paymentStatus: 'Unpaid',
			totalAmount: '$350.00',
			paymentMethod: 'Bank Transfer'
		},
		{
			invoice: 'INV004',
			paymentStatus: 'Paid',
			totalAmount: '$450.00',
			paymentMethod: 'Credit Card'
		},
		{
			invoice: 'INV005',
			paymentStatus: 'Paid',
			totalAmount: '$550.00',
			paymentMethod: 'PayPal'
		},
		{
			invoice: 'INV006',
			paymentStatus: 'Pending',
			totalAmount: '$200.00',
			paymentMethod: 'Bank Transfer'
		},
		{
			invoice: 'INV007',
			paymentStatus: 'Unpaid',
			totalAmount: '$300.00',
			paymentMethod: 'Credit Card'
		}
	];
</script>

<h1 class="text-2xl font-extrabold italic">Monitors</h1>

{open}
{JSON.stringify(selectedRowForDelete)}
<div class="my-8 rounded-lg border text-gray-500 shadow-md hover:text-black dark:text-white">
	<Table.Root>
		<Table.Header>
			<Table.Row>
				<Table.Head class="text-center italic text-black">Name</Table.Head>
				<Table.Head class="text-center italic text-black">URL</Table.Head>
				<Table.Head class="text-center italic text-black">Beats</Table.Head>
				<Table.Head class="w-24 text-center italic text-black">Frequency</Table.Head>
				<Table.Head class="w-24 text-center italic text-black">Action</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each invoices as invoice, i (i)}
				<Table.Row class="group">
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.invoice}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.paymentStatus}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black dark:text-white"
						>{invoice.paymentMethod}</Table.Cell
					>
					<Table.Cell class="-p-2 text-center text-gray-500 group-hover:text-black dark:text-white"
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
											variant="destructive"
											class="h-8 w-full"
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
