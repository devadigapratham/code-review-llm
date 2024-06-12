#!/usr/bin/env python
# coding: utf-8

# In[9]:




# In[10]:


from tree_sitter import Language, Parser






# In[12]:


# In[13]:


import tree_sitter_go as tsgo


# In[14]:


GO_LANGUAGE = Language(tsgo.language())


# In[16]:


parser = Parser(GO_LANGUAGE)
parser.language = GO_LANGUAGE 


# In[17]:


go_code = b"""

package main

import "fmt"

func main() {
	// Create a new website
	w := NewWebsite()

	// Add a few products
	p, err := NewProduct("Tide", 10, 100)
	if err != nil {
		fmt.Printf("Could not create product: %v\n", err)
		return
	}
	w.AddProduct(p)

	p, err = NewProduct("Tropicana", 100, 90)
	if err != nil {
		fmt.Printf("Could not create product: %v\n", err)
		return

	}
	w.AddProduct(p)

	p, err = NewProduct("Lays", 20, 10)
	if err != nil {
		fmt.Printf("Could not create product: %v\n", err)
		return
	}
	w.AddProduct(p)

	// Add a few customers
	c1, err := NewCustomer("Jack", "California")
	if err != nil {
		fmt.Printf("Could not create customer: %v\n", err)
		return
	}
	w.RegisterCustomer(c1)

	c2, err := NewCustomer("Ben", "London")
	if err != nil {
		fmt.Printf("Could not create customer: %v\n", err)
		return
	}
	w.RegisterCustomer(c2)

	// Do some transactions
	bill, err := w.Transact(c1, "Tide", 4)
	if err != nil {
		fmt.Printf("Could not generate bill amount: %v\n", err)
		return
	}
	fmt.Printf("Bill amount for %s is %s\n", c1.name, bill)

	bill, err = w.Transact(c2, "Tropicana", 10)
	if err != nil {
		fmt.Printf("Could not generate bill amount: %v\n", err)
		return
	}
	fmt.Printf("Bill amount for %s is %s\n", c2.name, bill)

	// Restock
	p, err = NewProduct("Tropicana", 10, 0)
	if err != nil {
		fmt.Printf("Could not create product: %v\n", err)
		return

	}
	w.AddProduct(p)

	p, err = NewProduct("Lays", 35, 20)
	if err != nil {
		fmt.Printf("Could not create product: %v\n", err)
		return
	}
	w.AddProduct(p)

	// Do some more transactions
	bill, err = w.Transact(c1, "Lays", 10)
	if err != nil {
		fmt.Printf("Could not generate bill amount: %v\n", err)
		return
	}
	fmt.Printf("Bill amount for %s is %s\n", c1.name, bill)

	bill, err = w.Transact(c1, "Tide", 20)
	if err != nil {
		fmt.Printf("Could not generate bill amount: %v\n", err)
		return
	}
	fmt.Printf("Bill amount for %s is %s\n", c1.name, bill)
}

type Website struct {
	customers []Customer
	products  map[string]Product
}

func NewWebsite() Website {
	return Website{
		customers: nil,
		products:  make(map[string]Product),
	}
}

func (w *Website) AddProduct(p Product) {
	if ep, ok := w.products[p.name]; !ok {
		if p.price == 0 {
			return
		}
		w.products[p.name] = p
	} else {
		if p.price != 0 {
			ep.price = p.price
		}
		ep.qty += p.qty
	}
}

func (w *Website) RegisterCustomer(c Customer) {
	for _, ec := range w.customers {
		if ec.name == c.name && ec.address == c.address {
			return
		}
	}
	w.customers = append(w.customers, c)
}

func (w *Website) Transact(c Customer, pName string, qty uint) (string, error) {
	defer func() {
		if p, ok := w.products[pName]; ok && p.qty == 0 {
			delete(w.products, pName)
		}
	}()

	p, ok := w.products[pName]
	if !ok {
		return "", fmt.Errorf("product '%s' does not exist", pName)
	}
	if p.qty < qty {
		return "", fmt.Errorf("not enough quantity for product: '%s'", p.name)
	}
	p.qty -= qty
	bill := fmt.Sprintf("%v x %v = %v", qty, p.price, qty*p.price)
	return bill, nil
}

type Customer struct {
	name    string
	address string
}

func NewCustomer(name, address string) (Customer, error) {
	if len(name) == 0 {
		return Customer{}, fmt.Errorf("name cannot be empty")
	}
	if len(address) == 0 {
		return Customer{}, fmt.Errorf("address cannot be empty")
	}
	if len(address) > 40 {
		return Customer{}, fmt.Errorf("address '%s' is longer than 40 characters", address)
	}
	return Customer{
		name:    name,
		address: address,
	}, nil
}

type Product struct {
	name  string
	qty   uint
	price uint
}

func NewProduct(name string, qty, price uint) (Product, error) {
	if len(name) == 0 {
		return Product{}, fmt.Errorf("name cannot be empty")
	}
	return Product{
		name:  name,
		qty:   qty,
		price: price,
	}, nil
}
"""


# In[18]:


tree = parser.parse(go_code)

# Explore the parsed syntax tree
root_node = tree.root_node

def print_node(node, indent=0):
    print('  ' * indent + node.type)
    for child in node.children:
        print_node(child, indent + 1)

# Print the syntax tree
print_node(root_node)

