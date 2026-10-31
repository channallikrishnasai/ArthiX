/**
 * Seed script — creates a realistic demo footwear retailer with ERP data.
 * Run: pnpm --filter @veska/core seed
 */
import '../load-env.js';
import { createDatabase } from './client.js';
import * as schema from './schema.js';
import { randomUUID } from 'node:crypto';
import { eq, sql } from 'drizzle-orm';
import bcrypt from 'bcrypt';

const DATABASE_URL = process.env['DATABASE_URL'];
if (!DATABASE_URL) {
  console.error('DATABASE_URL environment variable is required');
  process.exit(1);
}

const db = createDatabase(DATABASE_URL);

function days(n: number): Date {
  const d = new Date();
  d.setDate(d.getDate() + n);
  return d;
}

function isoDate(d: Date): string {
  return d.toISOString().slice(0, 10);
}

// /auth/login verifies with bcrypt.compare, so the seed must produce a bcrypt hash.
// It previously wrote a sha256 digest here, which bcrypt could never match.
function hashPassword(pw: string): string {
  return bcrypt.hashSync(pw, 10);
}

const DEMO_PW = hashPassword('demo1234');

async function seed() {
  console.log('Seeding StrideWorks Footwear demo data…');

  // ── Tenant ─────────────────────────────────────────────────────────────────
  const tenantId = randomUUID();

  // Check if demo tenant already exists
  const existing = await db.query.tenants.findFirst({
    where: eq(schema.tenants.slug, 'strideworks'),
  });

  if (existing) {
    console.log('Demo tenant already exists. Run seed:clear first to reset.');
    process.exit(0);
  }

  await db.insert(schema.tenants).values({
    id: tenantId,
    name: 'StrideWorks Footwear',
    slug: 'strideworks',
    timezone: 'America/New_York',
    defaultCurrency: 'USD',
    fiscalYearStart: '01-01',
  });
  console.log(`  Tenant created: ${tenantId}`);

  // ── Roles ──────────────────────────────────────────────────────────────────
  const adminRoleId = randomUUID();
  const hrRoleId = randomUUID();
  const financeRoleId = randomUUID();
  const employeeRoleId = randomUUID();

  await db.insert(schema.roles).values([
    {
      id: adminRoleId,
      tenantId,
      name: 'admin',
      description: 'Full access admin',
      capabilities: ['*'],
      isSystem: true,
    },
    {
      id: hrRoleId,
      tenantId,
      name: 'hr_manager',
      description: 'HR Manager',
      capabilities: ['hr:read', 'hr:write', 'payroll:read'],
      isSystem: false,
    },
    {
      id: financeRoleId,
      tenantId,
      name: 'finance',
      description: 'Finance team',
      capabilities: ['invoices:read', 'invoices:write', 'reports:read'],
      isSystem: false,
    },
    {
      id: employeeRoleId,
      tenantId,
      name: 'employee',
      description: 'Standard employee',
      capabilities: ['expenses:write', 'leave:write'],
      isSystem: false,
    },
  ]);
  console.log('  Roles created');

  // ── Identities (users) ─────────────────────────────────────────────────────
  const adminId = randomUUID();
  const hrId = randomUUID();
  const financeId = randomUUID();
  const johnId = randomUUID();

  await db.insert(schema.identities).values([
    {
      id: adminId,
      tenantId,
      type: 'user',
      channelIds: { email: 'admin@strideworks.com', passwordHash: DEMO_PW },
      roleIds: [adminRoleId],
      additionalCapabilities: ['*'],
      deniedCapabilities: [],
    },
    {
      id: hrId,
      tenantId,
      type: 'user',
      channelIds: { email: 'hr@strideworks.com', passwordHash: DEMO_PW },
      roleIds: [hrRoleId],
      additionalCapabilities: [],
      deniedCapabilities: [],
    },
    {
      id: financeId,
      tenantId,
      type: 'user',
      channelIds: { email: 'finance@strideworks.com', passwordHash: DEMO_PW },
      roleIds: [financeRoleId],
      additionalCapabilities: [],
      deniedCapabilities: [],
    },
    {
      id: johnId,
      tenantId,
      type: 'user',
      channelIds: { email: 'john@strideworks.com', passwordHash: DEMO_PW },
      roleIds: [employeeRoleId],
      additionalCapabilities: [],
      deniedCapabilities: [],
    },
  ]);

  // /auth/login authenticates against "users" (and sessions.userId references it),
  // while RBAC and channels key off "identities". The seed previously created only
  // identities, so the demo credentials could never log in. Create the matching
  // users rows, reusing the identity ids so userId and identityId line up.
  const demoUsers: Array<{ id: string; email: string; name: string; roleId: string }> = [
    { id: adminId, email: 'admin@strideworks.com', name: 'Admin User', roleId: adminRoleId },
    { id: hrId, email: 'hr@strideworks.com', name: 'HR Manager', roleId: hrRoleId },
    { id: financeId, email: 'finance@strideworks.com', name: 'Finance Manager', roleId: financeRoleId },
    { id: johnId, email: 'john@strideworks.com', name: 'John Employee', roleId: employeeRoleId },
  ];

  for (const u of demoUsers) {
    await db.execute(sql`
      INSERT INTO "users" ("id", "tenantId", "email", "name", "status", "passwordHash", "isActive")
      VALUES (${u.id}, ${tenantId}, ${u.email}, ${u.name}, 'active', ${DEMO_PW}, true)
      ON CONFLICT ("tenantId", "email") DO NOTHING
    `);

    // requirePermission() resolves capabilities via userRoles -> roles, so a user with
    // no userRoles row is denied everything (403) even if their identity grants '*'.
    await db.execute(sql`
      INSERT INTO "userRoles" ("userId", "roleId")
      VALUES (${u.id}, ${u.roleId})
      ON CONFLICT ("userId", "roleId") DO NOTHING
    `);
  }

  console.log('  Users created: admin@strideworks.com, hr@strideworks.com, finance@strideworks.com, john@strideworks.com');

  // ── Contacts (CRM) ─────────────────────────────────────────────────────────
  const contacts = [
    {
      firstName: 'Maya',
      lastName: 'Patel',
      email: 'maya@northstaroutfitters.example',
      phone: '+1-555-0101',
      company: 'Northstar Outfitters',
      title: 'Footwear Buyer',
    },
    {
      firstName: 'Andre',
      lastName: 'Lewis',
      email: 'andre@citystride.example',
      phone: '+1-555-0102',
      company: 'CityStride Stores',
      title: 'Retail Operations Director',
    },
    {
      firstName: 'Sofia',
      lastName: 'Martinez',
      email: 'sofia@trailhead.example',
      phone: '+1-555-0103',
      company: 'Trailhead Running Co.',
      title: 'Merchandising Manager',
    },
    {
      firstName: 'Ethan',
      lastName: 'Brooks',
      email: 'ethan@everydayfeet.example',
      phone: '+1-555-0104',
      company: 'Everyday Feet',
      title: 'Category Buyer',
    },
    {
      firstName: 'Nina',
      lastName: 'Shah',
      email: 'nina@juniorsteps.example',
      phone: '+1-555-0105',
      company: 'Junior Steps Kidswear',
      title: 'Store Owner',
    },
    {
      firstName: 'Oliver',
      lastName: 'Grant',
      email: 'oliver@peaktrail.example',
      phone: '+1-555-0106',
      company: 'Peak Trail Supply',
      title: 'Wholesale Director',
    },
    {
      firstName: 'Leah',
      lastName: 'Morgan',
      email: 'leah@harborwalk.example',
      phone: '+1-555-0107',
      company: 'Harbor Walk Boutique',
      title: 'Owner',
    },
    {
      firstName: 'Caleb',
      lastName: 'Reed',
      email: 'caleb@strideclub.example',
      phone: '+1-555-0108',
      company: 'Stride Club',
      title: 'Team Equipment Manager',
    },
  ];

  const contactIds: string[] = [];
  for (const c of contacts) {
    const id = randomUUID();
    contactIds.push(id);
    await db.insert(schema.entityRecords).values({
      id,
      tenantId,
      entityType: 'Contact',
      data: {
        ...c,
        status: 'active',
        source: 'manual',
        lastContacted: isoDate(days(-Math.floor(Math.random() * 30))),
        notes: `Key contact at ${c.company}`,
      },
      createdBy: adminId,
    });
  }
  console.log(`  Contacts created: ${contacts.length}`);

  // ── Deals (CRM) ────────────────────────────────────────────────────────────
  const dealStages = ['prospecting', 'qualification', 'proposal', 'negotiation', 'closed_won'];
  const deals = [
    { title: 'Northstar fall wholesale order', value: 85000, stage: 'closed_won', contactIndex: 0 },
    { title: 'CityStride store replenishment', value: 42000, stage: 'negotiation', contactIndex: 1 },
    { title: 'Everyday Feet trail-shoe launch', value: 120000, stage: 'proposal', contactIndex: 3 },
    { title: 'Peak Trail seasonal collection', value: 67500, stage: 'qualification', contactIndex: 5 },
    { title: 'Harbor Walk boutique order', value: 28000, stage: 'prospecting', contactIndex: 6 },
  ];

  for (const deal of deals) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'Deal',
      data: {
        title: deal.title,
        value: deal.value,
        currency: 'USD',
        stage: deal.stage,
        contactId: contactIds[deal.contactIndex],
        probability: dealStages.indexOf(deal.stage) * 20 + 10,
        expectedCloseDate: isoDate(days(deal.stage === 'closed_won' ? -15 : 30)),
        assignedTo: adminId,
        notes: `High-priority deal with ${deals[deal.contactIndex]?.title ?? deal.title}`,
      },
      createdBy: adminId,
    });
  }
  console.log(`  Deals created: ${deals.length}`);

  // ── Invoices ───────────────────────────────────────────────────────────────
  const invoiceData = [
    {
      number: 'INV-001',
      customerName: 'Northstar Outfitters',
      amount: 15000,
      status: 'paid',
      daysOffset: -60,
    },
    { number: 'INV-002', customerName: 'CityStride Stores', amount: 8500, status: 'paid', daysOffset: -45 },
    { number: 'INV-003', customerName: 'Everyday Feet', amount: 12000, status: 'sent', daysOffset: -30 },
    {
      number: 'INV-004',
      customerName: 'Junior Steps Kidswear',
      amount: 3200,
      status: 'overdue',
      daysOffset: -40,
    },
    {
      number: 'INV-005',
      customerName: 'Peak Trail Supply',
      amount: 9750,
      status: 'sent',
      daysOffset: -20,
    },
    {
      number: 'INV-006',
      customerName: 'Harbor Walk Boutique',
      amount: 5500,
      status: 'draft',
      daysOffset: -5,
    },
    {
      number: 'INV-007',
      customerName: 'Stride Club',
      amount: 2100,
      status: 'overdue',
      daysOffset: -55,
    },
    {
      number: 'INV-008',
      customerName: 'Trailhead Running Co.',
      amount: 14200,
      status: 'paid',
      daysOffset: -70,
    },
    {
      number: 'INV-009',
      customerName: 'Northstar Outfitters',
      amount: 6800,
      status: 'sent',
      daysOffset: -10,
    },
    { number: 'INV-010', customerName: 'CityStride Stores', amount: 500, status: 'draft', daysOffset: -2 },
  ];

  for (const inv of invoiceData) {
    const issueDate = days(inv.daysOffset);
    const dueDate = new Date(issueDate);
    dueDate.setDate(dueDate.getDate() + 30);

    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'Invoice',
      data: {
        number: inv.number,
        customerName: inv.customerName,
        amount: inv.amount,
        currency: 'USD',
        status: inv.status,
        issueDate: isoDate(issueDate),
        dueDate: isoDate(dueDate),
        lineItems: [
          {
            description: `Footwear wholesale order ${inv.number}`,
            quantity: 1,
            unitPrice: inv.amount,
            total: inv.amount,
          },
        ],
        notes: inv.status === 'overdue' ? 'Payment overdue — follow up required' : '',
        paidAt: inv.status === 'paid' ? isoDate(days(inv.daysOffset + 20)) : null,
      },
      createdBy: financeId,
    });
  }
  console.log(`  Invoices created: ${invoiceData.length}`);

  // ── Expenses ───────────────────────────────────────────────────────────────
  const expenseData = [
    { title: 'Leather and sole samples', amount: 842, category: 'Materials', status: 'approved' },
    { title: 'Freight for spring collection', amount: 2400, category: 'Shipping', status: 'approved' },
    { title: 'Retail team planning lunch', amount: 187, category: 'Meals', status: 'approved' },
    { title: 'Warehouse shoe racks (x3)', amount: 1650, category: 'Equipment', status: 'submitted' },
    { title: 'Product photography props', amount: 520, category: 'Marketing', status: 'submitted' },
    { title: 'Courier — sample shipment', amount: 64, category: 'Shipping', status: 'draft' },
    { title: 'Footwear trade show booth', amount: 1800, category: 'Marketing', status: 'approved' },
    { title: 'Materials sourcing trip', amount: 1299, category: 'Travel', status: 'draft' },
  ];

  for (let i = 0; i < expenseData.length; i++) {
    const exp = expenseData[i]!;
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'Expense',
      data: {
        ...exp,
        currency: 'USD',
        employeeId: johnId,
        employeeName: 'John Doe',
        submittedAt: exp.status !== 'draft' ? isoDate(days(-10 - i * 3)) : null,
        approvedAt: exp.status === 'approved' ? isoDate(days(-8 - i * 3)) : null,
        receipt: exp.status !== 'draft' ? `receipt-${i + 1}.pdf` : null,
      },
      createdBy: johnId,
    });
  }
  console.log(`  Expenses created: ${expenseData.length}`);

  // ── Employees (HR) ─────────────────────────────────────────────────────────
  const employeeData = [
    {
      firstName: 'Sarah',
      lastName: 'Chen',
      email: 'schen@strideworks.com',
      department: 'Product',
      position: 'Footwear Designer',
      salary: 140000,
      startDate: isoDate(days(-730)),
    },
    {
      firstName: 'Marcus',
      lastName: 'Williams',
      email: 'mwilliams@strideworks.com',
      department: 'Sales',
      position: 'Wholesale Account Manager',
      salary: 95000,
      startDate: isoDate(days(-365)),
    },
    {
      firstName: 'Priya',
      lastName: 'Patel',
      email: 'ppatel@strideworks.com',
      department: 'Merchandising',
      position: 'Merchandising Manager',
      salary: 125000,
      startDate: isoDate(days(-540)),
    },
    {
      firstName: 'James',
      lastName: "O'Brien",
      email: 'jobrien@strideworks.com',
      department: 'Finance',
      position: 'Finance Analyst',
      salary: 105000,
      startDate: isoDate(days(-820)),
    },
    {
      firstName: 'Aisha',
      lastName: 'Johnson',
      email: 'ajohnson@strideworks.com',
      department: 'HR',
      position: 'People Operations Manager',
      salary: 98000,
      startDate: isoDate(days(-270)),
    },
    {
      firstName: 'John',
      lastName: 'Doe',
      email: 'john@strideworks.com',
      department: 'Warehouse',
      position: 'Warehouse Coordinator',
      salary: 115000,
      startDate: isoDate(days(-180)),
    },
  ];

  const employeeRecordIds: string[] = [];
  for (const emp of employeeData) {
    const id = randomUUID();
    employeeRecordIds.push(id);
    await db.insert(schema.entityRecords).values({
      id,
      tenantId,
      entityType: 'Employee',
      data: {
        ...emp,
        status: 'active',
        employeeNumber: `EMP-${String(employeeRecordIds.length).padStart(3, '0')}`,
        currency: 'USD',
        payFrequency: 'monthly',
      },
      createdBy: hrId,
    });
  }
  console.log(`  Employees created: ${employeeData.length}`);

  // ── Leave Requests ─────────────────────────────────────────────────────────
  const leaveData = [
    {
      employeeIdx: 0,
      type: 'Annual Leave',
      startDate: isoDate(days(14)),
      endDate: isoDate(days(21)),
      status: 'approved',
      days: 5,
    },
    {
      employeeIdx: 2,
      type: 'Annual Leave',
      startDate: isoDate(days(7)),
      endDate: isoDate(days(9)),
      status: 'pending',
      days: 3,
    },
    {
      employeeIdx: 3,
      type: 'Sick Leave',
      startDate: isoDate(days(-5)),
      endDate: isoDate(days(-3)),
      status: 'approved',
      days: 3,
    },
    {
      employeeIdx: 5,
      type: 'Annual Leave',
      startDate: isoDate(days(30)),
      endDate: isoDate(days(37)),
      status: 'pending',
      days: 5,
    },
  ];

  for (const leave of leaveData) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'LeaveRequest',
      data: {
        ...leave,
        employeeId: employeeRecordIds[leave.employeeIdx],
        employeeName:
          `${employeeData[leave.employeeIdx]?.firstName ?? ''} ${employeeData[leave.employeeIdx]?.lastName ?? ''}`.trim(),
        reason: leave.type === 'Sick Leave' ? 'Flu recovery' : 'Personal vacation',
        approvedBy: leave.status === 'approved' ? hrId : null,
        approvedAt: leave.status === 'approved' ? isoDate(days(-2)) : null,
      },
      createdBy: employeeRecordIds[leave.employeeIdx] ?? hrId,
    });
  }
  console.log(`  Leave requests created: ${leaveData.length}`);

  // ── Projects ────────────────────────────────────────────────────────────────
  const projectData = [
    {
      name: 'Spring footwear collection',
      status: 'active',
      startDate: isoDate(days(-45)),
      endDate: isoDate(days(60)),
      tasks: [
        { title: 'Finalize running-shoe prototypes', status: 'done', assigneeIdx: 2 },
        { title: 'Approve colors and materials', status: 'in_progress', assigneeIdx: 0 },
        { title: 'Fit testing across sizes', status: 'todo', assigneeIdx: 0 },
        { title: 'Send collection to retailers', status: 'todo', assigneeIdx: 2 },
      ],
    },
    {
      name: 'Warehouse layout refresh',
      status: 'completed',
      startDate: isoDate(days(-180)),
      endDate: isoDate(days(-30)),
      tasks: [
        { title: 'Map current stock locations', status: 'done', assigneeIdx: 2 },
        { title: 'Install size-labeled shelving', status: 'done', assigneeIdx: 0 },
        { title: 'Update picking workflow', status: 'done', assigneeIdx: 5 },
        { title: 'Train warehouse team', status: 'done', assigneeIdx: 2 },
      ],
    },
    {
      name: 'Wholesale portal improvements',
      status: 'planning',
      startDate: isoDate(days(30)),
      endDate: isoDate(days(180)),
      tasks: [
        { title: 'Collect retailer feedback', status: 'todo', assigneeIdx: 2 },
        { title: 'Add size-run ordering', status: 'todo', assigneeIdx: 3 },
        { title: 'Review delivery tracking options', status: 'todo', assigneeIdx: 2 },
      ],
    },
  ];

  for (const proj of projectData) {
    const projectId = randomUUID();
    await db.insert(schema.entityRecords).values({
      id: projectId,
      tenantId,
      entityType: 'Project',
      data: {
        name: proj.name,
        status: proj.status,
        startDate: proj.startDate,
        endDate: proj.endDate,
        budget: 50000,
        currency: 'USD',
        managerId: adminId,
        description: `${proj.name} project`,
        taskCount: proj.tasks.length,
        completedTaskCount: proj.tasks.filter((t) => t.status === 'done').length,
      },
      createdBy: adminId,
    });

    for (const task of proj.tasks) {
      await db.insert(schema.entityRecords).values({
        id: randomUUID(),
        tenantId,
        entityType: 'Task',
        data: {
          title: task.title,
          status: task.status,
          projectId,
          assigneeId: employeeRecordIds[task.assigneeIdx],
          assigneeName:
            `${employeeData[task.assigneeIdx]?.firstName ?? ''} ${employeeData[task.assigneeIdx]?.lastName ?? ''}`.trim(),
          priority: 'medium',
          dueDate: proj.endDate,
        },
        createdBy: adminId,
      });
    }
  }
  console.log(
    `  Projects created: ${projectData.length} with ${projectData.reduce((s, p) => s + p.tasks.length, 0)} tasks`,
  );

  // ── Support Tickets ────────────────────────────────────────────────────────
  const ticketData = [
    { subject: 'Wholesale order arrived with missing sizes', priority: 'high', status: 'open', contactIdx: 3 },
    {
      subject: 'Invoice #INV-003 has a quantity mismatch',
      priority: 'medium',
      status: 'in_progress',
      contactIdx: 2,
    },
    { subject: 'Trail shoes run smaller than expected', priority: 'high', status: 'open', contactIdx: 0 },
    { subject: 'Request to exchange a pair for another size', priority: 'low', status: 'resolved', contactIdx: 4 },
    {
      subject: 'Need an updated wholesale catalog',
      priority: 'low',
      status: 'resolved',
      contactIdx: 5,
    },
  ];

  for (const ticket of ticketData) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'SupportTicket',
      data: {
        subject: ticket.subject,
        priority: ticket.priority,
        status: ticket.status,
        contactId: contactIds[ticket.contactIdx],
        contactName:
          `${contacts[ticket.contactIdx]?.firstName ?? ''} ${contacts[ticket.contactIdx]?.lastName ?? ''}`.trim(),
        assignedTo: adminId,
        resolvedAt: ticket.status === 'resolved' ? isoDate(days(-3)) : null,
        channel: 'email',
        tags: [ticket.priority, ticket.status],
      },
      createdBy: adminId,
    });
  }
  console.log(`  Support tickets created: ${ticketData.length}`);

  // ── Knowledge Base Articles ────────────────────────────────────────────────
  const kbArticles = [
    {
      title: 'Getting Started with StrideWorks',
      slug: 'getting-started',
      content:
        '# Getting Started\n\nWelcome to ArthiX! This guide will walk you through the initial setup.\n\n## Step 1: Create your tenant\n...\n\n## Step 2: Invite users\n...',
      category: 'Onboarding',
      status: 'published',
    },
    {
      title: 'How to Create an Invoice',
      slug: 'create-invoice',
      content:
        '# Creating Invoices\n\nInvoices can be created from the Finance module.\n\n## Steps\n1. Navigate to Finance > Invoices\n2. Click "New Invoice"\n3. Fill in customer details\n...',
      category: 'Finance',
      status: 'published',
    },
    {
      title: 'Leave Policy',
      slug: 'leave-policy',
      content:
        '# Leave Policy\n\nStrideWorks Footwear provides competitive leave entitlements.\n\n## Annual Leave\nAll employees receive 20 days of annual leave per year.\n\n## Sick Leave\nUp to 10 days of paid sick leave per year.\n...',
      category: 'HR',
      status: 'published',
    },
  ];

  for (const article of kbArticles) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'KBArticle',
      data: {
        ...article,
        authorId: adminId,
        authorName: 'Admin',
        views: Math.floor(Math.random() * 200) + 10,
        helpful: Math.floor(Math.random() * 40) + 5,
        publishedAt: isoDate(days(-30)),
        updatedAt: isoDate(days(-7)),
        tags: [article.category.toLowerCase(), 'guide'],
      },
      createdBy: adminId,
    });
  }
  console.log(`  KB articles created: ${kbArticles.length}`);

  // ── Inventory Items ────────────────────────────────────────────────────────
  const inventoryData = [
    {
      name: 'StrideFlex Road Runner',
      sku: 'SFR-001',
      price: 124,
      cost: 48,
      stock: 180,
      reorderLevel: 40,
      category: 'Running Shoes',
    },
    {
      name: 'StrideFlex Trail Runner',
      sku: 'SFT-002',
      price: 139,
      cost: 56,
      stock: 96,
      reorderLevel: 30,
      category: 'Trail Shoes',
    },
    {
      name: 'Everyday Canvas Low',
      sku: 'ECL-003',
      price: 74,
      cost: 25,
      stock: 240,
      reorderLevel: 50,
      category: 'Casual Shoes',
    },
    {
      name: 'Junior Steps School Shoe',
      sku: 'JSS-004',
      price: 59,
      cost: 22,
      stock: 23,
      reorderLevel: 35,
      category: 'Kids Shoes',
    },
    {
      name: 'Harbor Walk Leather Loafer',
      sku: 'HWL-005',
      price: 158,
      cost: 62,
      stock: 8,
      reorderLevel: 15,
      category: 'Dress Shoes',
    },
  ];

  for (const item of inventoryData) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'InventoryItem',
      data: {
        name: item.name,
        sku: item.sku,
        price: item.price,
        cost: item.cost,
        stockQuantity: item.stock,
        reorderLevel: item.reorderLevel,
        category: item.category,
        status: 'active',
        currency: 'USD',
        unit: 'pair',
        warehouseId: 'warehouse-main',
        description: `${item.name} — standard product`,
      },
      createdBy: adminId,
    });
  }
  console.log(`  Inventory items created: ${inventoryData.length}`);

  // ── Sales orders ───────────────────────────────────────────────────────────
  // The dashboard counts SalesOrder, PurchaseOrder, PayrollRun and TimeEntry rows.
  // None of them were seeded, so four tiles always read zero and the Sales,
  // Purchasing, Payroll and Time pages opened empty.
  const salesOrders = [
    { number: 'SO-1001', customer: 'Northstar Outfitters', amount: 24500, status: 'confirmed' },
    { number: 'SO-1002', customer: 'CityStride Stores', amount: 8900, status: 'pending' },
    { number: 'SO-1003', customer: 'Everyday Feet', amount: 41200, status: 'shipped' },
    { number: 'SO-1004', customer: 'Junior Steps Kidswear', amount: 3150, status: 'delivered' },
    { number: 'SO-1005', customer: 'Peak Trail Supply', amount: 17800, status: 'confirmed' },
  ];
  for (const o of salesOrders) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'SalesOrder',
      data: {
        orderNumber: o.number,
        customerName: o.customer,
        amount: o.amount,
        currency: 'USD',
        status: o.status,
        orderDate: isoDate(days(-Math.floor(Math.random() * 20) - 1)),
        expectedDelivery: isoDate(days(Math.floor(Math.random() * 21) + 3)),
      },
      createdBy: adminId,
    });
  }
  console.log(`  Sales orders created: ${salesOrders.length}`);

  // ── Purchase orders ────────────────────────────────────────────────────────
  const purchaseOrders = [
    { number: 'PO-2001', vendor: 'Harbor Sole Works', amount: 12400, status: 'ordered' },
    { number: 'PO-2002', vendor: 'Northstar Leather Supply', amount: 3600, status: 'draft' },
    { number: 'PO-2003', vendor: 'Evergreen Recycled Textiles', amount: 8750, status: 'ordered' },
    { number: 'PO-2004', vendor: 'SwiftStep Logistics', amount: 2100, status: 'received' },
  ];
  for (const o of purchaseOrders) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'PurchaseOrder',
      data: {
        orderNumber: o.number,
        vendorName: o.vendor,
        amount: o.amount,
        currency: 'USD',
        status: o.status,
        orderDate: isoDate(days(-Math.floor(Math.random() * 25) - 1)),
      },
      createdBy: adminId,
    });
  }
  console.log(`  Purchase orders created: ${purchaseOrders.length}`);

  // ── Payroll runs (this month, so the dashboard tile is non-zero) ───────────
  const payrollRuns = [
    { period: 'Current month — first half', gross: 48200, employees: 6, status: 'completed' },
    { period: 'Current month — second half', gross: 48200, employees: 6, status: 'draft' },
  ];
  for (const r of payrollRuns) {
    await db.insert(schema.entityRecords).values({
      id: randomUUID(),
      tenantId,
      entityType: 'PayrollRun',
      data: {
        period: r.period,
        grossAmount: r.gross,
        netAmount: Math.round(r.gross * 0.78),
        employeeCount: r.employees,
        currency: 'USD',
        status: r.status,
      },
      createdBy: adminId,
    });
  }
  console.log(`  Payroll runs created: ${payrollRuns.length}`);

  // ── Time entries (this week) ───────────────────────────────────────────────
  const timeTasks = [
    'Review new shoe samples',
    'Call wholesale retailers',
    'Reconcile store invoices',
    'Resolve size exchange requests',
    'Plan the spring collection',
    'Negotiate leather supply order',
  ];
  let timeCount = 0;
  for (const userId of [adminId, hrId, financeId, johnId]) {
    for (let i = 0; i < 2; i++) {
      await db.insert(schema.entityRecords).values({
        id: randomUUID(),
        tenantId,
        entityType: 'TimeEntry',
        data: {
          userId,
          description: timeTasks[(timeCount + i) % timeTasks.length],
          hours: [2, 3.5, 4, 6, 7.5][Math.floor(Math.random() * 5)],
          billable: i % 2 === 0,
          date: isoDate(new Date()),
        },
        createdBy: userId,
      });
      timeCount++;
    }
  }
  console.log(`  Time entries created: ${timeCount}`);

  // ── Approval chain + pending requests ──────────────────────────────────────
  // Without a chain nothing ever routes for sign-off, so the approvals inbox was
  // empty and money-moving actions had no gate at all out of the box.
  const chainId = randomUUID();
  await db.execute(sql`
    INSERT INTO "approvalChains" ("id", "tenantId", "name", "entityType", "conditionField",
      "conditionOp", "conditionValue", "steps", "enabled")
    VALUES (${chainId}, ${tenantId}, 'Expenses over $500', 'expense', 'amount', 'gt', 500,
      ${JSON.stringify([{ order: 1, approverRole: 'finance', label: 'Finance review' }])}::jsonb, true)
  `);

  const pendingApprovals = [
    { type: 'Expense', title: 'Expense: Client dinner — $780' },
    { type: 'Expense', title: 'Expense: Conference travel — $1,240' },
    { type: 'PurchaseOrder', title: 'PO-2001: Harbor Sole Works — $12,400' },
  ];
  for (const a of pendingApprovals) {
    await db.execute(sql`
      INSERT INTO "approvalRequests" ("id", "tenantId", "chainId", "entityType", "entityId",
        "entityTitle", "currentStep", "totalSteps", "status", "requestedBy")
      VALUES (${randomUUID()}, ${tenantId}, ${chainId}, ${a.type}, ${randomUUID()},
        ${a.title}, 1, 1, 'pending', ${johnId})
    `);
  }
  console.log(`  Approval chain + ${pendingApprovals.length} pending requests created`);

  console.log('\nSeed complete! Login credentials:');
  console.log('  admin@strideworks.com   / demo1234  (Admin)');
  console.log('  hr@strideworks.com      / demo1234  (HR Manager)');
  console.log('  finance@strideworks.com / demo1234  (Finance)');
  console.log('  john@strideworks.com    / demo1234  (Employee)');

  console.log('\nSign in at http://localhost:3000, no further configuration needed.');
}

seed()
  .then(() => process.exit(0))
  .catch((err: unknown) => {
    console.error('Seed failed:', err);
    process.exit(1);
  });
