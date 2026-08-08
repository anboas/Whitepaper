---
title: "Software Policy Should Raise the Floor"
date: 2026-08-08
summary: "A draft note on why the Department of War has many software-adjacent policies, but still needs a common policy floor for good software development."
status: draft
type: note
tags:
  - software-policy
  - defense
  - devsecops
  - acquisition
  - software-modernization
  - governance
---

# Software Policy Should Raise the Floor

_The Department has many policies around software. It still needs policy for the discipline of building good software._

The Department of War does not lack documents that mention software.

It has acquisition policy for software-intensive programs. It has cybersecurity policy. It has Risk Management Framework policy. It has test and evaluation policy. It has digital engineering policy. It has DevSecOps reference material, software modernization strategy, cloud strategy, cyber requirements, data rules, contracting pathways, and pockets of real engineering excellence across the Services and agencies.

That is not the same thing as software policy.

At least not in the sense that matters.

Most of the existing policy landscape governs the things around software: how software is bought, authorized, secured, tested, engineered into larger systems, funded, reviewed, and reported. Those are necessary disciplines. They are not sufficient to define the Department's default approach to building, sustaining, measuring, and improving good software.

The gap is not that nobody in the Department knows how to build software. That would be false. There are outstanding teams, software factories, platform groups, cyber operators, acquisition leaders, and mission organizations that already understand modern delivery. The gap is that excellence is unevenly distributed. Too much depends on local leadership, heroic teams, unusual authorities, special contracting vehicles, and communities of practice that have to keep re-winning arguments the Department should have settled years ago.

Software policy should raise the floor.

It should not flatten the high performers. It should make their practices less exceptional.

## The Gap Is Real, But It Is Not Empty

The strongest version of the claim is not "there is no software policy."

There is.

DoD Instruction 5000.87 created the Software Acquisition Pathway and requires programs using that pathway to employ modern iterative software development methodologies, DevSecOps, human-centered design, collaboration with users, and recurring delivery of capabilities to operations [1]. That matters.

DoD Instruction 5000.89 establishes test and evaluation policy across acquisition pathways, including the Software Acquisition Pathway [2]. That matters too.

DoD Instruction 5000.90 focuses acquisition decision authorities and program managers on cybersecurity responsibilities across the acquisition lifecycle [3]. DoD Instruction 8510.01 establishes the Risk Management Framework for DoD systems and connects cybersecurity risk to acquisition, test, evaluation, operations, and sustainment [4]. DoD Instruction 8500.01 establishes cybersecurity policy for the DoD information enterprise [5].

DoD Instruction 5000.97 establishes digital engineering policy and responsibilities across the acquisition lifecycle [6]. The DoD Software Modernization Strategy emphasizes cloud, DevSecOps, cybersecurity, and workforce as major enablers for resilient software delivery [7].

So the Department is not operating in a policy vacuum.

But the center of gravity is still fragmented. One document is about acquisition pathway governance. Another is about test. Another is about cybersecurity. Another is about RMF. Another is about digital engineering. Strategic documents point in the right direction, but strategy is not the same as a management instruction. Reference designs and communities of practice help capable teams, but they do not create a common Department-wide quality floor.

The more precise claim is this:

The Department has software-adjacent policy, but it has not had a coherent instruction-level management system for software development quality.

That is the missing layer.

## Why Software-Adjacent Policy Is Not Enough

Software is now one of the main ways military capability changes after fielding.

That changes the policy problem.

If software is treated mainly as an acquisition object, policy will optimize for pathways, approvals, strategies, and delivery cadence. If it is treated mainly as a cybersecurity object, policy will optimize for controls, risk acceptance, authorization, and vulnerability management. If it is treated mainly as a test object, policy will optimize for verification, evaluation, adequacy, and evidence. If it is treated mainly as a digital engineering object, policy will optimize for models, authoritative sources of truth, technical baselines, and lifecycle engineering evidence.

All of those views are valid. None of them is complete.

The act of building good software has its own management discipline. It requires user discovery, backlog discipline, architecture choices, code quality, automated testing, CI/CD, observability, secure supply chains, incident learning, production telemetry, reusable platforms, team health, documentation, interface discipline, dependency management, and a real feedback loop between users, engineers, security, test, acquisition, and operators.

When policy does not articulate that discipline, the Department gets predictable failure modes.

Programs can say they are agile while still managing work through slow approval rituals.

Teams can say they use DevSecOps while treating the pipeline as a compliance artifact instead of a delivery system.

Organizations can pass cyber review while still producing brittle, unmaintainable software.

Program offices can deliver increments while failing to learn from users.

Contractors can meet requirements while leaving the government with poor technical leverage.

Leaders can brief dashboards while having no reliable signal about code health, delivery friction, operational use, or maintainability.

That is the problem a real software policy should address.

## The Point Is a Quality Floor

The purpose of software policy is not to tell every team which framework, language, vendor tool, sprint ritual, or pipeline product to use.

That would be the wrong level of control.

The point is to define the Department's minimum expectations for responsible software development, then give teams enough room to satisfy those expectations in mission-appropriate ways.

A good policy floor would make several things normal.

Working software should be the primary evidence of progress.

Users should be continuously involved, not consulted at the beginning and disappointed at the end.

Software should be delivered in small increments that can be tested, secured, observed, and improved.

Automated testing should be expected, including unit, integration, security, performance, and mission-relevant tests where appropriate.

CI/CD should be treated as a management system for repeatable delivery and evidence generation, not only as a technical toolchain.

Security should be built into development from the start, with software supply chain risk, secrets handling, dependency management, vulnerability response, and authorization evidence integrated into delivery.

Code quality should be visible enough to manage. That includes maintainability, review discipline, technical debt, defect trends, architecture drift, interface stability, and documentation that helps future teams operate the system.

Operational telemetry should feed development priorities. Teams should know whether software is used, where it fails, what users struggle with, and what mission outcome is improving.

Reusable platforms, shared services, and common components should be preferred where they improve speed, security, interoperability, and government leverage.

Government teams should preserve technical insight and decision rights. Software policy should make it harder to outsource understanding.

Metrics should measure delivery health, quality, security, user value, and operational performance. They should not reward theater.

None of this is exotic. It is the ordinary discipline of modern software organizations.

The Department's problem is not that these practices are unknown. The problem is that they are not yet ubiquitous enough to be assumed.

## Pockets of Excellence Are Not a System

Pockets of excellence are valuable, but they are also evidence of a system gap.

If the Department can point to excellent software teams, that proves the practices are feasible inside the defense environment. It does not prove the environment reliably produces them.

That distinction matters.

A serious enterprise cannot depend on scattered exceptions for a core capability. It cannot require every program to rediscover user-centered development, platform leverage, automated testing, DevSecOps evidence, modern contracting, and operational telemetry from scratch. It cannot treat software delivery competence as a personality trait of unusually good leaders.

The policy goal should be to make competence portable.

That means turning lessons from high-performing teams into default expectations. It means making software quality legible to senior leaders without reducing it to shallow compliance. It means creating enough common vocabulary that acquisition, cyber, test, engineering, operations, and development teams can inspect the same delivery system instead of arguing from separate policy worlds.

The policy should not ask every team to become identical.

It should ask every team to be credible.

## Good Software Policy Is a Management System

The best software policy would not read like a coding standard.

It would read like a management system for continuous capability delivery.

It would define who is accountable for software outcomes. It would require programs to maintain an inspectable delivery model. It would connect acquisition strategy, technical architecture, user feedback, cyber authorization, test evidence, sustainment, and operational telemetry into one loop.

It would ask plain questions.

Who are the users, and how does the team learn from them?

How often does working software reach an operationally meaningful environment?

What evidence shows the software is secure enough, reliable enough, usable enough, and maintainable enough?

What does the pipeline prove?

What manual steps still block delivery?

What parts of the architecture are reusable, replaceable, observable, and owned by the government?

What technical debt is being accepted, by whom, and with what operational consequence?

What changed because users touched the software?

What can leadership see before the program becomes a rescue operation?

These are policy questions because they shape behavior, accountability, funding, oversight, and authority.

Software quality is not only an engineering virtue. In the Department, it is a governance problem.

## The Coming Instruction Has a Chance to Matter

The coming DoD Instruction can matter if it fills the missing layer instead of adding another adjacent lane.

It should consolidate and clarify where the Department already has policy coverage, but its real value would be establishing a common operating model for software development quality across pathways and organizations.

The test is simple.

After the instruction lands, does a program office know what good software development should look like?

Does a commander know what signals matter?

Does an acquisition leader know what to require without overprescribing implementation?

Does a cyber organization know how its evidence connects to continuous delivery?

Does a test organization know how to use automated and iterative evidence without waiting for late-stage ceremony?

Does a software team know what the Department expects as a baseline?

Does the government retain enough technical insight to manage the thing it is buying?

If the answer is yes, the policy will have done more than add paperwork. It will have raised the Department's default expectations.

## The Real Thesis

The Department does not need software policy because no one has ever written about software.

It needs software policy because software has become too central to military capability for quality to remain local, optional, or personality-driven.

The Department already has many ways to govern software from the outside. Acquisition governs the pathway. Cyber governs the risk. Test governs the evidence. Digital engineering governs the lifecycle model. Strategy governs the aspiration.

The missing layer is the software development quality floor.

That floor should not be glamorous. It should be ordinary, inspectable, and hard to avoid. It should make working software, user feedback, automated evidence, delivery discipline, code quality, security integration, observability, and continuous improvement normal across the enterprise.

That was the point of the software policy effort.

Not to invent good software development.

Not to centralize every method.

Not to punish teams already doing the work well.

The point was to raise the noise floor so that good software development stopped being a pocket of excellence and started becoming the Department's default expectation.

That is what software policy should do.

It should make the minimum better.

## Sources

1. U.S. Department of Defense, [DoD Instruction 5000.87, Operation of the Software Acquisition Pathway](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500087p.pdf), 2020.
2. U.S. Department of Defense, [DoD Instruction 5000.89, Test and Evaluation](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500089p.pdf), 2020.
3. U.S. Department of Defense, [DoD Instruction 5000.90, Cybersecurity for Acquisition Decision Authorities and Program Managers](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500090p.pdf), 2020.
4. U.S. Department of Defense, [DoD Instruction 8510.01, Risk Management Framework for DoD Systems](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/851001p.pdf), 2022.
5. U.S. Department of Defense, [DoD Instruction 8500.01, Cybersecurity](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/850001_2014.pdf), 2014.
6. U.S. Department of Defense, [DoD Instruction 5000.97, Digital Engineering](https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/500097p.pdf), 2023.
7. U.S. Department of Defense, [DoD Software Modernization Strategy](https://media.defense.gov/2022/Feb/03/2002932833/-1/-1/1/DOD-SOFTWARE-MODERNIZATION-STRATEGY.PDF), 2022.
