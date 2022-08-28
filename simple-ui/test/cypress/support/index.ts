// ***********************************************************
// This example support/index.ts is processed and
// loaded automatically before your e2e test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

import './commands';
import '@cypress/code-coverage/support';

Cypress.Commands.add('dropNode', (library, name, x?, y?) => {
  cy.url().then((url) => {
    if (!url.endsWith('#/') && !url.endsWith('#/canvas')) {
      cy.visit('/');
    }
  });
  cy.get('.q-drawer').then((drawer) => {
    if (drawer.css('visibility') == 'hidden') {
      cy.dataCy('leftDrawer').click();
    }
  });
  cy.dataCy('treeNode')
    .contains(name)
    .then((root) => {
      if (!root.is(':visible')) {
        cy.dataCy('treeRoot')
          .contains(`Library: ${library}`)
          .click()
          .then(() => {
            cy.wrap(root).click();
          });
      }
    });
  const node = cy.dataCy('treeNode').contains(name);
  const dataTransfer = new DataTransfer();
  node.trigger('dragstart', { dataTransfer });
  cy.dataCy('canvas').trigger('drop', {
    dataTransfer,
    offsetX: x == null ? 0 : x,
    offsetY: y == null ? 0 : y,
  });
  if (!(library == 'Base' && name == 'CustomNode')) {
    cy.dataCy('okBtn').click();
  }
});
