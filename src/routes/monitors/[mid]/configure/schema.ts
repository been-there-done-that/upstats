import { z } from 'zod';

export const formSchema = z.object({
	name: z.string().min(2).max(50),
	url: z.string().url(),
	method: z.string().min(3).default('GET'),
	frequency: z.number().default(43200)
});

export type FormSchema = typeof formSchema;
