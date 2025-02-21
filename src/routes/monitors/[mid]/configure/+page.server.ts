import type { Actions, PageLoad } from './$types';
import { superValidate } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
import { BASE_URL } from '$env/static/private';

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const load: PageLoad = async ({ params }) => {
	console.log({ config: params });
	return {
		form: await superValidate(zod(formSchema)),
		id: '121212',
		name: 'Google',
		url: 'http://google.com',
		status: 'SUCCESS',
		paused: false,
		beats: [
			{ id: '1', date: '2025-02-15T10:27:01Z', status_code: 400 },
			{
				id: '2',
				date: '2025-02-15T10:28:01Z',
				status_code: 200
			},
			{
				id: '3',
				date: '2025-02-15T10:29:01Z',
				status_code: 200
			}
		],
		frequency: '5 Minutes'
	};
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		return {
			form
		};
	}
};
