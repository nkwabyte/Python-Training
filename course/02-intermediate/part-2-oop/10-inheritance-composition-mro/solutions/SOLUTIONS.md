# Solutions & Commentary — Module 10: Inheritance, Composition, and MRO

## Key Takeaways
- Favor composition over inheritance: compose objects by passing dependencies into `__init__` rather than building deep inheritance hierarchies.
- Understand Method Resolution Order (MRO) with C3 Linearization via `ClassName.mro()`.
- Always use `super().__init__()` with cooperative multiple inheritance.
